# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

#!/usr/bin/env python3
import os
import random
import string

import azure.core.credentials
import azure.core.pipeline
import azure.identity

import azure.mgmt.servicelinker
import azure.mgmt.resource

import azure.mgmt.appplatform
import azure.mgmt.sql

import azure.mgmt.web
import azure.mgmt.keyvault
import azure.mgmt.msi


# The Service Linker provider need user token in a separated header in the following scenarios.
#   * The target resource is Key Vault
#   * SecretStore is used to store secret in Key Vault
#   * VNetSolutionInfo is specified
class UserTokenPolicy(azure.core.pipeline._base.HTTPPolicy):
    USER_TOKEN_HEADER = 'x-ms-serviceconnector-user-token'
    AUTHORIZATION_HEADER = 'Authorization'
    BEARER_TOKEN_PREFIX = 'bearer '

    def __init__(self, credential: azure.core.credentials.TokenCredential, scope = 'https://management.azure.com//.default'):
        self._credential = credential
        self._scope = scope

    def send(self, request):
        headers = request.http_request.headers
        authorization = headers[self.AUTHORIZATION_HEADER]
        if isinstance(authorization, str) and authorization.lower().startswith(self.BEARER_TOKEN_PREFIX):
            headers[self.USER_TOKEN_HEADER] = authorization[len(self.BEARER_TOKEN_PREFIX):]
        else:
            token = self._credential.get_token(self._scope)
            headers[self.USER_TOKEN_HEADER] = token.token
        return self.next.send(request)


def random_string(length: int) -> str:
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))


# Setup connection between Spring Cloud App and SQL Database using username and password by creating Service Linker
def create_spring_cloud_and_sql_connection(credential: azure.core.credentials.TokenCredential, SUBSCRIPTION_ID: str, RESOURCE_GROUP_NAME: str):
    RESOURCE_GROUP_NAME = RESOURCE_GROUP_NAME or 'rg' + random_string(8)
    REGION = 'eastus'
    SPRING_SERVICE_NAME = 'spring' + random_string(8)
    SPRING_APP_NAME = 'app' + random_string(8)
    SQL_SERVER_NAME = 'sqlserver' + random_string(8)
    SQL_DATABASE_NAME = 'sqldb' + random_string(8)
    SQL_USER_NAME = 'sql' + random_string(8)
    SQL_PASSWORD = '5$Ql' + random_string(8)
    LINKER_NAME = 'sql'

    resource_client = azure.mgmt.resource.ResourceManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    app_platform_client = azure.mgmt.appplatform.AppPlatformManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    sql_client = azure.mgmt.sql.SqlManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    service_linker_client = azure.mgmt.servicelinker.ServiceLinkerManagementClient(
        credential,
    )

    # Create Spring Cloud App and Deployment
    resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME,
        {
            'location': REGION,
        }
    )
    app_platform_client.services.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SPRING_SERVICE_NAME,
        {
            'location': REGION,
        }
    ).result()
    app_platform_client.apps.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SPRING_SERVICE_NAME,
        SPRING_APP_NAME,
        {}
    ).result()
    deployment = app_platform_client.deployments.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SPRING_SERVICE_NAME,
        SPRING_APP_NAME,
        'default',
        {
            'properties': {
                'source': {
                    'type': 'jar',
                    'relative_path': '<default>'
                }
            }
        }
    ).result()
    print('created spring cloud deployment: {}'.format(deployment.id))

    # Create SQL Database
    sql_client.servers.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SQL_SERVER_NAME,
        {
            'location': REGION,
            'administrator_login': SQL_USER_NAME,
            'administrator_login_password': SQL_PASSWORD,
        }
    ).result()
    sql_database = sql_client.databases.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SQL_SERVER_NAME,
        SQL_DATABASE_NAME,
        {
            'location': REGION,
        }
    ).result()
    print('created sql database: {}'.format(sql_database.id))

    # Setup connection between Spring Cloud App and SQL Database using username and password by creating Service Linker
    linker = service_linker_client.linker.begin_create_or_update(
        deployment.id,
        LINKER_NAME,
        {
            'targetService': {
                'type': 'AzureResource',
                'id': sql_database.id,
            },
            'authInfo': {
                'authType': 'secret',
                'name': SQL_USER_NAME,
                'secretInfo': {
                    'secretType': 'rawValue',
                    'value': SQL_PASSWORD,
                },
            },
            'clientType': 'django',
        },
    ).result()
    print('created service linker: {}'.format(linker.id))

    # List Configurations of the connection
    configuration =  service_linker_client.linker.list_configurations(
        deployment.id,
        LINKER_NAME,
    )

    print('Configurations:')
    for config in configuration.configurations:
        print('\t{}: {}'.format(config.name, config.value))


# Setup connection between Web App and Key Vault using User Assigned Identity by creating Service Linker
def create_web_app_and_key_vault_connection(credential: azure.core.credentials.TokenCredential, SUBSCRIPTION_ID: str, TENANT_ID: str, RESOURCE_GROUP_NAME: str):
    RESOURCE_GROUP_NAME = RESOURCE_GROUP_NAME or 'rg' + random_string(8)
    REGION = 'eastus'
    WEB_APP_PLAN_NAME = 'plan' + random_string(8)
    WEB_APP_NAME = 'web' + random_string(8)
    KEY_VAULT_NAME = 'vault' + random_string(8)
    IDENTITY_NAME = 'identity' + random_string(8)
    LINKER_NAME = 'keyvault'

    resource_client = azure.mgmt.resource.ResourceManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    web_client = azure.mgmt.web.WebSiteManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    key_vault_client = azure.mgmt.keyvault.KeyVaultManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )
    msi_client = azure.mgmt.msi.ManagedServiceIdentityClient(
        credential,
        SUBSCRIPTION_ID,
    )
    service_linker_client = azure.mgmt.servicelinker.ServiceLinkerManagementClient(
        credential,
        per_retry_policies = UserTokenPolicy(credential),
    )

    # Create Web App
    resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME,
        {
            'location': REGION,
        }
    )
    web_app_plan = web_client.app_service_plans.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        WEB_APP_PLAN_NAME,
        {
            'location': REGION,
            'sku': {
                'name': 'B1',
            },
        }
    ).result()
    web_app = web_client.web_apps.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        WEB_APP_NAME,
        {
            'location': REGION,
            'properties': {
                'serverFarmId': web_app_plan.id,
            },
        }
    ).result()
    print('created web app: {}'.format(web_app.id))

    # Create Key Vault
    key_vault = key_vault_client.vaults.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        KEY_VAULT_NAME,
        {
            'location': REGION,
            'properties': {
                'TENANT_ID': TENANT_ID,
                'sku': {
                    'family': 'A',
                    'name': 'Standard',
                },
                'accessPolicies': [],
            },
        }
    ).result()
    print('created key vault: {}'.format(key_vault.id))

    # Create User Assigned Identity
    identity = msi_client.user_assigned_identities.create_or_update(
        RESOURCE_GROUP_NAME,
        IDENTITY_NAME,
        {
            'location': REGION,
        }
    )
    print('created user assigned identity: {}, client_id: {}'.format(identity.id, identity.client_id))

    # Setup connection between Web App and Key Vault using User Assigned Identity by creating Service Linker
    linker = service_linker_client.linker.begin_create_or_update(
        web_app.id,
        LINKER_NAME,
        {
            'targetService': {
                'type': 'AzureResource',
                'id': key_vault.id,
            },
            'authInfo': {
                'authType': 'userAssignedIdentity',
                'client_id': identity.client_id,
                'SUBSCRIPTION_ID': SUBSCRIPTION_ID,
            },
            'clientType': 'python',
        },
    ).result()
    print('created service linker: {}'.format(linker.id))

    # List Configurations of the connection
    configuration =  service_linker_client.linker.list_configurations(
        web_app.id,
        LINKER_NAME,
    )

    print('Configurations:')
    for config in configuration.configurations:
        print('\t{}: {}'.format(config.name, config.value))


def main():
    credential = azure.identity.DefaultAzureCredential()
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TENANT_ID = os.environ.get("AZURE_TENANT_ID", None)
    RESOURCE_GROUP_NAME = 'rg' + random_string(8)
    try:
        create_spring_cloud_and_sql_connection(credential, SUBSCRIPTION_ID, RESOURCE_GROUP_NAME)
        create_web_app_and_key_vault_connection(credential, SUBSCRIPTION_ID, TENANT_ID, RESOURCE_GROUP_NAME)
    finally:
        # Delete Resource Group to clean up all resources
        azure.mgmt.resource.ResourceManagementClient(credential, SUBSCRIPTION_ID).resource_groups.begin_delete(RESOURCE_GROUP_NAME)


if __name__ == '__main__':
    main()

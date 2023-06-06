# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
from dateutil import parser as date_parse

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    PASSWORD = os.environ.get("PASSWORD", None)
    TENANT_ID = os.environ.get("TENANT_ID", None)
    CLIENT_OID = os.environ.get("CLIENT_OID", None)
    GROUP_NAME = "testgroupx"
    SERVER_KEY = "server_keyxxyyzz"
    SERVER_KEY_TYPE = "AzureKeyVault"
    SERVER = "serverxxy"
    VAULT = "vaultxxy"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    sql_client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    keyvault_client = KeyVaultManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create Server
    server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
          },
          "administrator_login": "dummylogin",
          "administrator_login_password": PASSWORD,
          "version": "12.0",
          "public_network_access":"Enabled"
        }
    ).result()
    print("Create server:\n{}".format(server))

    # Create vault
    vault = keyvault_client.vaults.begin_create_or_update(
        GROUP_NAME,
        VAULT,
        {
            'location': "eastus",
            'properties': {
                'sku': {
                    'family': 'A',
                    'name': 'standard'
                },
                'tenant_id': TENANT_ID,
                "access_policies": [
                    {
                    "tenant_id": TENANT_ID,
                    "object_id": CLIENT_OID,
                    "permissions": {
                        "keys": [
                        "get",
                        "create",
                        "delete",
                        "list",
                        "update",
                        "import",
                        "backup",
                        "restore",
                        "recover"
                        ],
                        "secrets": [
                        "get",
                        "list",
                        "set",
                        "delete",
                        "backup",
                        "restore",
                        "recover"
                        ],
                        "certificates": [
                        "get",
                        "list",
                        "delete",
                        "create",
                        "import",
                        "update",
                        "managecontacts",
                        "getissuers",
                        "listissuers",
                        "setissuers",
                        "deleteissuers",
                        "manageissuers",
                        "recover"
                        ],
                        "storage": [
                        "get",
                        "list",
                        "delete",
                        "set",
                        "update",
                        "regeneratekey",
                        "setsas",
                        "listsas",
                        "getsas",
                        "deletesas"
                        ]
                    }
                    },
                    {
                    "tenantId": TENANT_ID,
                    "objectId": server.identity.principal_id,
                    "permissions": {
                        "keys": [
                        "unwrapKey",
                        "get",
                        "wrapKey",
                        "list"
                        ]
                    }
                    }
                ],
                'enabled_for_disk_encryption': True,
                'enable_soft_delete': True,
                'soft_delete_retention_in_days': 90,
                'nework_acls': {
                    'bypass': 'AzureServices',
                    'default_action': "Allow",
                    'ip_rules': [],
                    'virtual_network_rules': []
                }
            }
        }
    ).result()

    key_client = KeyClient(
        vault.properties.vault_uri,
        DefaultAzureCredential()
    )

    key = key_client.create_key(
        "testkey",
        "RSA",
        size=2048,
        expires_on=date_parse.parse("2050-02-02T08:00:00.000Z")
    )
    SERVER_KEY = VAULT + "_testkey_" + key.id.split("/")[-1]
    # - end -

    # Create server key
    server_key = sql_client.server_keys.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        SERVER_KEY,
        {
            # TODO: init resource body
            "server_key_type": SERVER_KEY_TYPE,
            "uri": key.id
        }
    ).result()
    print("Create server key:\n{}".format(server_key))
    
    # Set encryptrion protector
    sql_client.encryption_protectors.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        "current",
        {
            "server_key_name":SERVER_KEY,
            "server_key_type":SERVER_KEY_TYPE
        }
    )
    
    # Get server key
    server_key = sql_client.server_keys.get(
        GROUP_NAME,
        SERVER,
        SERVER_KEY
    )
    print("Get server key:\n{}".format(server_key))

    # Delete server key
    server_key = sql_client.server_keys.begin_delete(
        GROUP_NAME,
        SERVER,
        SERVER_KEY
    ).result()
    print("Delete server key.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

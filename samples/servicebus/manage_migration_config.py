# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE = "namespacexxyyzz"
    NAMESPACE_PRIMARY = "namespaceprimaryxxyyzz"
    AUTHORIZATION_RULE_NAME = "myAuthorizationRule"
    MIGRATION_CONFIG = "$default"
    POST_MIGRATION_NAME = "postmigrationxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    servicebus_client = ServiceBusManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create namespace
    namespace = servicebus_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "eastus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    # Create namespace primary
    second_namespace = servicebus_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE_PRIMARY,
        {
          "sku": {
            "name": "Premium",
            "tier": "Premium"
          },
          "location": "westus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    # Create namespace authorization rule
    rule = servicebus_client.namespaces.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        AUTHORIZATION_RULE_NAME,
        {
          "rights": [
            "Listen",
            "Send"
          ]
        }
    )
    # - end -

    # Create migration config
    migration_config = servicebus_client.migration_configs.begin_create_and_start_migration(
        GROUP_NAME,
        NAMESPACE,
        MIGRATION_CONFIG,
        {
          "target_namespace": second_namespace.id,
          "post_migration_name": POST_MIGRATION_NAME
        }
    ).result()
    print("Create migration config:\n{}".format(migration_config))

    # Complete migration config
    result = servicebus_client.migration_configs.complete_migration(
        GROUP_NAME,
        NAMESPACE,
        MIGRATION_CONFIG
    )
    print("Complete migration config.\n")  

    # Get migration config
    migration_config = servicebus_client.migration_configs.get(
        GROUP_NAME,
        NAMESPACE,
        MIGRATION_CONFIG
    )
    count = 0
    while migration_config.provisioning_state != "Succeeded" and count<10:
        time.sleep(30)
        migration_config = servicebus_client.migration_configs.get(
            GROUP_NAME,
            NAMESPACE,
            MIGRATION_CONFIG
        )
        count += 1
    print("Get migration config:\n{}".format(migration_config))

    # Delete migration config
    try:
        migration_config = servicebus_client.migration_configs.delete(
            GROUP_NAME,
            NAMESPACE,
            MIGRATION_CONFIG
        )
    except HttpResponseError as e:
        if not str(e).startswith("(NotFound)"):
            raise e
    print("Delete migration config.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

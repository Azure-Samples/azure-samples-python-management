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
    NAMESPACE = "myNamespacexxyyzzzy"
    NAMESPACE_PRIMARY = "myNamespacexxyyzzzysecond"
    AUTHORIZATION_RULE_NAME = "myAuthorizationRule"
    DISASTER_RECOVERY_CONFIG = "mydisasterrecovercf"

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
            "name": "Premium",
            "tier": "Premium"
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

    # Check name availability
    result = servicebus_client.disaster_recovery_configs.check_name_availability(
        GROUP_NAME,
        NAMESPACE,
        {
            "name": DISASTER_RECOVERY_CONFIG
        }
    )

    # Create disaster recovery config
    disaster_recovery_config = servicebus_client.disaster_recovery_configs.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        DISASTER_RECOVERY_CONFIG,
        {
            "partner_namespace": second_namespace.id
        }
    )
    print("Create disaster recovery config:\n{}".format(disaster_recovery_config))

    # Get disaster recovery config
    disaster_recovery_config = servicebus_client.disaster_recovery_configs.get(
        GROUP_NAME,
        NAMESPACE,
        DISASTER_RECOVERY_CONFIG
    )
    count = 0
    while disaster_recovery_config.provisioning_state != "Succeeded" and count<10:
        time.sleep(30)
        disaster_recovery_config = servicebus_client.disaster_recovery_configs.get(
            GROUP_NAME,
            NAMESPACE,
            DISASTER_RECOVERY_CONFIG
        )
        count += 1
    print("Get disaster recovery config:\n{}".format(disaster_recovery_config))

    # Fail over
    result = servicebus_client.disaster_recovery_configs.fail_over(
        GROUP_NAME,
        NAMESPACE_PRIMARY,
        DISASTER_RECOVERY_CONFIG
    )
    print("Fail over disaster recovery config.\n")
    
    # Delete disaster recovery config
    count = 0
    while count<10:
        try:
            disaster_recovery_config = servicebus_client.disaster_recovery_configs.delete(
                GROUP_NAME,
                NAMESPACE_PRIMARY,
                DISASTER_RECOVERY_CONFIG
            )
        except HttpResponseError:
            time.sleep(30)
            count += 1
        else:
            break
    print("Delete disaster recovery config.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

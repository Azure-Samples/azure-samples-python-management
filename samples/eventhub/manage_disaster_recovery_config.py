# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import time

from azure.identity import DefaultAzureCredential
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import HttpResponseError


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE_NAME = "namespacex"
    NAMESPACE_NAME_2 = "namespacextwo"
    DISASTER_RECOVERY_CONFIG_NAME = "disasterrecoveryconfig"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    eventhub_client = EventHubManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Namespace
    eventhub_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
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

    # Create Second Namespace
    second_namespace = eventhub_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME_2,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "westus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    # Check name availability
    result = eventhub_client.disaster_recovery_configs.check_name_availability(
        GROUP_NAME,
        NAMESPACE_NAME,
        {
          "name": NAMESPACE_NAME_2
        }
    )
    print("Check name availability: {}".format(result))

    # Create disaster recovery config
    config = eventhub_client.disaster_recovery_configs.create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
        DISASTER_RECOVERY_CONFIG_NAME,
        {
          "partner_namespace": second_namespace.id
        }
    )
    print("Create disaster recovery config: {}".format(config))

    # Get disaster recovery config
    for _ in range(5):
        config = eventhub_client.disaster_recovery_configs.get(
            GROUP_NAME,
            NAMESPACE_NAME,
            DISASTER_RECOVERY_CONFIG_NAME
        )
        if config.provisioning_state == "Successed":
            break
        time.sleep(30)
    print("Get disaster recovery config: {}".format(config))

    # Break pairing disaster recovery config
    eventhub_client.disaster_recovery_configs.break_pairing(
        GROUP_NAME,
        NAMESPACE_NAME,
        DISASTER_RECOVERY_CONFIG_NAME
    )
    print("Break pairing disaster recovery config.")

    # Fail over disaster recovery config
    eventhub_client.disaster_recovery_configs.fail_over(
        GROUP_NAME,
        NAMESPACE_NAME_2,
        DISASTER_RECOVERY_CONFIG_NAME
    )
    print("Fail over disaster recovery config.")

    # Delete disaster recovery config
    for _ in range(5):
        try:
            eventhub_client.disaster_recovery_configs.delete(
                GROUP_NAME,
                NAMESPACE_NAME,
                DISASTER_RECOVERY_CONFIG_NAME
            )
        except HttpResponseError:
            time.sleep(30)
        else:
            break
    print("Delete disaster recovery config.")

    # Delete Namespace
    eventhub_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE_NAME
    ).result()

    # Delete Second Namespace
    eventhub_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE_NAME_2
    ).result()

    # Delete resource group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

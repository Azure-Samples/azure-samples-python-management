# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    DDOS_PROTECTION_PLAN = "ddos_protection_planxxyyzz"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create ddos protection plan
    ddos_protection_plan = network_client.ddos_protection_plans.begin_create_or_update(
        GROUP_NAME,
        DDOS_PROTECTION_PLAN,
        {
          "location": "westus"
        }
    ).result()
    print("Create ddos protection plan:\n{}".format(ddos_protection_plan))

    # Get ddos protection plan
    ddos_protection_plan = network_client.ddos_protection_plans.get(
        GROUP_NAME,
        DDOS_PROTECTION_PLAN
    )
    print("Get ddos protection plan:\n{}".format(ddos_protection_plan))

    # Update ddos protection plan
    ddos_protection_plan = network_client.ddos_protection_plans.update_tags(
        GROUP_NAME,
        DDOS_PROTECTION_PLAN,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update ddos protection plan:\n{}".format(ddos_protection_plan))
    
    # Delete ddos protection plan
    ddos_protection_plan = network_client.ddos_protection_plans.begin_delete(
        GROUP_NAME,
        DDOS_PROTECTION_PLAN
    ).result()
    print("Delete ddos protection plan.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


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
    IP_GROUP = "ip_groupxxyyzz"

    # Create client
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

    # Create ip group
    ip_group = network_client.ip_groups.begin_create_or_update(
        GROUP_NAME,
        IP_GROUP,
        {
          "tags": {
            "key1": "value1"
          },
          "location": "West US",
          "ip_addresses": [
            "13.64.39.16/32",
            "40.74.146.80/31",
            "40.74.147.32/28"
          ]
        }
    ).result()
    print("Create ip group:\n{}".format(ip_group))

    # Get ip group
    ip_group = network_client.ip_groups.get(
        GROUP_NAME,
        IP_GROUP
    )
    print("Get ip group:\n{}".format(ip_group))
    
    # Delete ip group
    ip_group = network_client.ip_groups.begin_delete(
        GROUP_NAME,
        IP_GROUP
    ).result()
    print("Delete ip group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

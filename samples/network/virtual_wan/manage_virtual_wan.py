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
    VIRTUAL_WAN = "virtual_wanxxyyzz"

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

    # Create virtual wan
    virtual_wan = network_client.virtual_wans.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_WAN,
        {
          "location": "West US",
          "tags": {
            "key1": "value1"
          },
          "disable_vpn_encryption": False,
          "type": "Basic"
        }
    ).result()
    print("Create virtual wan:\n{}".format(virtual_wan))

    # Get virtual wan
    virtual_wan = network_client.virtual_wans.get(
        GROUP_NAME,
        VIRTUAL_WAN
    )
    print("Get virtual wan:\n{}".format(virtual_wan))

    # Update virtual wan
    virtual_wan = network_client.virtual_wans.update_tags(
        GROUP_NAME,
        VIRTUAL_WAN,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update virtual wan:\n{}".format(virtual_wan))
    
    # Delete virtual wan
    virtual_wan = network_client.virtual_wans.begin_delete(
        GROUP_NAME,
        VIRTUAL_WAN
    ).result()
    print("Delete virtual wan.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

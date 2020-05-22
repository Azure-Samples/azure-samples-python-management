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
    VIRTUAL_HUB = "virtual_hubxxyyzz"
    VIRTUAL_WAN = "virtual_wanxxyzz"

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

    # - init depended resources -
    # Create virtual wan
    network_client.virtual_wans.begin_create_or_update(
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
    # - end -

    # Create virtual hub
    virtual_hub = network_client.virtual_hubs.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_HUB,
        {
          "location": "West US",
          "tags": {
            "key1": "value1"
          },
          "virtual_wan": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualWans/" + VIRTUAL_WAN + ""
          },
          "address_prefix": "10.168.0.0/24",
          "sku": "Basic"
        }
    ).result()
    print("Create virtual hub:\n{}".format(virtual_hub))

    # Get virtual hub
    virtual_hub = network_client.virtual_hubs.get(
        GROUP_NAME,
        VIRTUAL_HUB
    )
    print("Get virtual hub:\n{}".format(virtual_hub))

    # Update virtual hub
    virtual_hub = network_client.virtual_hubs.update_tags(
        GROUP_NAME,
        VIRTUAL_HUB,
        {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    )
    print("Update virtual hub:\n{}".format(virtual_hub))
    
    # Delete virtual hub
    virtual_hub = network_client.virtual_hubs.begin_delete(
        GROUP_NAME,
        VIRTUAL_HUB
    ).result()
    print("Delete virtual hub.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

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
    VIRTUAL_NETWORK_NAME = "virtualnetwork"

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

    # Create virtual network
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "location": "eastus"
        }
    ).result()
    print("Create virtual network:\n{}".format(network))

    # Get virtual network
    network = network_client.virtual_networks.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME
    )
    print("Get virtual network:\n{}".format(network))

    # Update virtual network tags
    network = network_client.virtual_networks.update_tags(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update virtual network tags:\n{}".format(network))

    # Delete virtual network
    network_client.virtual_networks.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME
    ).result()
    print("Delete virtual network.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

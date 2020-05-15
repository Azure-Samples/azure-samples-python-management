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
    NETWORK_PROFILE = "network_profilexxyyzz"
    VIRTUAL_NETWORK_NAME = "virtualnetworkxx"
    SUBNET = "subnetxxx"

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

    # - init depended resources -
    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
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

    # Create subnet
    network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET,
        {
          "address_prefix": "10.0.0.0/24"
        }
    ).result()
    # - end -

    # Create network profile
    network_profile = network_client.network_profiles.create_or_update(
        GROUP_NAME,
        NETWORK_PROFILE,
        {
          "location": "eastus",
          "container_network_interface_configurations": [
            {
              "name": "eth1",
              "ip_configurations": [
                {
                  "name": "ipconfig1",
                  "subnet": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET + ""
                  }
                }
              ]
            }
          ]
        }
    )
    print("Create network profile:\n{}".format(network_profile))

    # Get network profile
    network_profile = network_client.network_profiles.get(
        GROUP_NAME,
        NETWORK_PROFILE
    )
    print("Get network profile:\n{}".format(network_profile))

    # Update network profile
    network_profile = network_client.network_profiles.update_tags(
        GROUP_NAME,
        NETWORK_PROFILE,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update network profile:\n{}".format(network_profile))
    
    # Delete network profile
    network_profile = network_client.network_profiles.begin_delete(
        GROUP_NAME,
        NETWORK_PROFILE
    ).result()
    print("Delete network profile.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

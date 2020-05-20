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
    NETWORK_INTERFACE = "network_interfacexxyyzz"
    PUBLIC_IP_ADDRESS_NAME = "publicipaddress"
    VIRTUAL_NETWORK_NAME = "virtualnetworkxx"
    SUBNET_NAME = "subnetxxx"
    IP_CONFIGURATION_NAME = "ipconfigurationxx"

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
    # Create public ip address
    network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS_NAME,
        {
            'location': "eastus",
            'public_ip_allocation_method': 'Static',
            'idle_timeout_in_minutes': 4,
            'sku': {
              'name': 'Standard'
            }
        }
    ).result()

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
        SUBNET_NAME,
        {
          "address_prefix": "10.0.0.0/24"
        }
    ).result()
    # - end -

    # Create network interface
    network_interface = network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        NETWORK_INTERFACE,
        {
          "enable_accelerated_networking": True,
          "ip_configurations": [
            {
              "name": IP_CONFIGURATION_NAME,
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              },
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/"+ SUBNET_NAME
              }
            }
          ],
          "location": "eastus"
        }
    ).result()
    print("Create network interface:\n{}".format(network_interface))

    # Get network interface
    network_interface = network_client.network_interfaces.get(
        GROUP_NAME,
        NETWORK_INTERFACE
    )
    print("Get network interface:\n{}".format(network_interface))

    # Update network interface
    network_interface = network_client.network_interfaces.update_tags(
        GROUP_NAME,
        NETWORK_INTERFACE,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update network interface:\n{}".format(network_interface))
    
    # Delete network interface
    network_interface = network_client.network_interfaces.begin_delete(
        GROUP_NAME,
        NETWORK_INTERFACE
    ).result()
    print("Delete network interface.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

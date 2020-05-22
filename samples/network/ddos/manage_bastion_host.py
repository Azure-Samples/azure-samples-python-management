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
    BASTION_HOST = "bastion_hostxxyyzz"
    PUBLIC_IP_ADDRESS_NAME = "publicipaddress"
    BASTION_VIRTUAL_NETWORK_NAME = "virtualnetworkxx"
    BASTION_SUBNET_NAME = "AzureBastionSubnet"  # must be AzureBastionSubnet

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
    )

    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        BASTION_VIRTUAL_NETWORK_NAME,
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
        BASTION_VIRTUAL_NETWORK_NAME,
        BASTION_SUBNET_NAME,
        {
          "address_prefix": "10.0.0.0/24"
        }
    ).result()
    # - end -

    # Create bastion host
    bastion_host = network_client.bastion_hosts.begin_create_or_update(
        GROUP_NAME,
        BASTION_HOST,
        {
          "location": "eastus",
          "ip_configurations": [
            {
              "name": "bastionHostIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + BASTION_VIRTUAL_NETWORK_NAME + "/subnets/" + BASTION_SUBNET_NAME + ""
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME + ""
              }
            }
          ]
        }
    ).result()
    print("Create bastion host:\n{}".format(bastion_host))

    # Get bastion host
    bastion_host = network_client.bastion_hosts.get(
        GROUP_NAME,
        BASTION_HOST
    )
    print("Get bastion host:\n{}".format(bastion_host))
    
    # Delete bastion host
    bastion_host = network_client.bastion_hosts.begin_delete(
        GROUP_NAME,
        BASTION_HOST
    ).result()
    print("Delete bastion host.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

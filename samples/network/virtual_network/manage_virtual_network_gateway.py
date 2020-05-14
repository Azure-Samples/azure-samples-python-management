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
    VIRTUAL_NETWORK_GATEWAY = "virtual_network_gatewayxxyyzz"
    IP_CONFIGURATION_NAME = "ipconfigurationxx"
    VIRTUAL_NETWORK_NAME = "virtualnetworkxx"
    SUBNET = "GatewaySubnet"  # Must be `GatewaySubnet`
    PUBLIC_IP_ADDRESS_NAME = "publicipaddressxxxx"

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
    network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS_NAME,
        {
            'location': "eastus",
            'public_ip_allocation_method': 'Dynamic',
            'idle_timeout_in_minutes': 4
        }
    )

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

    # Create virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY,
        {
          "ip_configurations": [
            {
              "private_ip_allocation_method": "Dynamic",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET + ""
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME + ""
              },
              "name": IP_CONFIGURATION_NAME
            }
          ],
          "gateway_type": "Vpn",
          "vpn_type": "RouteBased",
          "enable_bgp": False,
          "active_active": False,
          "enable_dns_forwarding": False,
          "sku": {
            "name": "VpnGw1",
            "tier": "VpnGw1"
          },
          "bgp_settings": {
            "asn": "65515",
            "bgp_peering_address": "10.0.1.30",
            "peer_weight": "0"
          },
          "custom_routes": {
            "address_prefixes": [
              "101.168.0.6/32"
            ]
          },
          "location": "eastus"
        }
    ).result()
    print("Create virtual network gateway:\n{}".format(virtual_network_gateway))

    # Get virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY
    )
    print("Get virtual network gateway:\n{}".format(virtual_network_gateway))

    # Update virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.begin_update_tags(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()
    print("Update virtual network gateway:\n{}".format(virtual_network_gateway))
    
    # Delete virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY
    ).result()
    print("Delete virtual network gateway.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

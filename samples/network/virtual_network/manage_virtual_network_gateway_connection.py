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
    VIRTUAL_NETWORK_GATEWAY_CONNECTION = "virtual_network_gateway_connectionxxyyzz"
    PUBLIC_IP_ADDRESS_NAME = "publicipaddress"
    VIRTUAL_NETWORK_NAME = "virtualnetworkxxx"
    GATEWAY_SUBNET = "GatewaySubnet"  # Must be `GatewaySubnet`
    VIRTUAL_NETWORK_GATEWAY = "virtualnetworkgatewayxx"
    LOCAL_NETWORK_GATEWAY = "localnetworkgatewayxx"
    IP_CONFIGURATION_NAME  = "ipconfigurationxxx"

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
    # - init depended client -
    # - end -

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
            'public_ip_allocation_method': 'Dynamic',
            'idle_timeout_in_minutes': 4
        }
    )

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
        GATEWAY_SUBNET,
        {
          "address_prefix": "10.0.0.0/24"
        }
    ).result()

    # Create virtual network gateway
    network_client.virtual_network_gateways.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY,
        {
          "ip_configurations": [
            {
              "private_ip_allocation_method": "Dynamic",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + GATEWAY_SUBNET + ""
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

    # Create local network gateway
    network_client.local_network_gateways.begin_create_or_update(
        GROUP_NAME,
        LOCAL_NETWORK_GATEWAY,
        {
          "local_network_address_space": {
            "address_prefixes": [
              "10.1.0.0/16"
            ]
          },
          "gateway_ip_address": "11.12.13.14",
          "location": "eastus"
        }
    ).result()
    # - end -

    # Create virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION,
        {
          "virtual_network_gateway1": {
            "ip_configurations": [
              {
                "private_ip_allocation_method": "Dynamic",
                "subnet": {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + GATEWAY_SUBNET + ""
                },
                "public_ip_address": {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME + ""
                },
                "name": IP_CONFIGURATION_NAME,
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY + "/ipConfigurations/" + IP_CONFIGURATION_NAME + ""
              }
            ],
            "gateway_type": "Vpn",
            "vpn_type": "RouteBased",
            "enable_bgp": False,
            "active_active": False,
            "sku": {
              "name": "VpnGw1",
              "tier": "VpnGw1"
            },
            "bgp_settings": {
              "asn": "65514",
              "bgp_peering_address": "10.0.2.30",
              "peer_weight": "0"
            },
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY + "",
            "location": "eastus"
          },
          "local_network_gateway2": {
            "local_network_address_space": {
              "address_prefixes": [
                "10.1.0.0/16"
              ]
            },
            "gateway_ip_address": "10.1.0.1",
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/localNetworkGateways/" + LOCAL_NETWORK_GATEWAY + "",
            "location": "eastus"
          },
          "connection_type": "IPsec",
          "connection_protocol": "IKEv2",
          "routing_weight": "0",
          "shared_key": "Abc123",
          "enable_bgp": False,
          "use_policy_based_traffic_selectors": False,
          "ipsec_policies": [],
          "traffic_selector_policies": [],
          "location": "eastus"
        }
    ).result()
    print("Create virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))

    # Get virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION
    )
    print("Get virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))

    # Update virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_update_tags(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()
    print("Update virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))
    
    # Delete virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION
    ).result()
    print("Delete virtual network gateway connection.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

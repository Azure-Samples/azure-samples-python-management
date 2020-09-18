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
    VPN_GATEWAY = "vpn_gatewayxxyyzz"
    VIRTUAL_WAN = "virtualwanxxx"
    VIRTUAL_HUB = "virtualhubxxxx"
    VPN_SITE = "vpnsitexxx"
    VPN_SITE_LINK = "vpnSiteLink1"

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

    # Create virtual hub
    network_client.virtual_hubs.begin_create_or_update(
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

    # Create vpn site
    network_client.vpn_sites.begin_create_or_update(
        GROUP_NAME,
        VPN_SITE,
        {
          "tags": {
            "key1": "value1"
          },
          "location": "West US",
          "virtual_wan": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualWans/" + VIRTUAL_WAN + ""
          },
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "is_security_site": False,
          "vpn_site_links": [
            {
              "name": VPN_SITE_LINK,
              "ip_address": "50.50.50.56",
              "link_properties": {
                "link_provider_name": "vendor1",
                "link_speed_in_mbps": "0"
              },
              "bgp_properties": {
                "bgp_peering_address": "192.168.0.0",
                "asn": "1234"
              }
            }
          ]
        }
    ).result()
    # - end -

    # Create vpn gateway
    vpn_gateway = network_client.vpn_gateways.begin_create_or_update(
        GROUP_NAME,
        VPN_GATEWAY,
        {
          "location": "West US",
          "tags": {
            "key1": "value1"
          },
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB + ""
          },
          "connections": [
            {
              "name": "vpnConnection1",
              "remote_vpn_site": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE + ""
              },
              "vpn_link_connections": [
                {
                  "name": "Connection-Link1",
                  "vpn_site_link": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE + "/vpnSiteLinks/" + VPN_SITE_LINK + ""
                  },
                  "connection_bandwidth": "200",
                  "vpn_connection_protocol_type": "IKEv2",
                  "shared_key": "key"
                }
              ]
            }
          ],
          "bgp_settings": {
            "asn": "65515",
            "peer_weight": "0"
          }
        }
    ).result()
    print("Create vpn gateway:\n{}".format(vpn_gateway))

    # Get vpn gateway
    vpn_gateway = network_client.vpn_gateways.get(
        GROUP_NAME,
        VPN_GATEWAY
    )
    print("Get vpn gateway:\n{}".format(vpn_gateway))

    # Update vpn gateway
    vpn_gateway = network_client.vpn_gateways.begin_update_tags(
        GROUP_NAME,
        VPN_GATEWAY,
        {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    ).result()
    print("Update vpn gateway:\n{}".format(vpn_gateway))
    
    # Delete vpn gateway
    vpn_gateway = network_client.vpn_gateways.begin_delete(
        GROUP_NAME,
        VPN_GATEWAY
    ).result()
    print("Delete vpn gateway.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

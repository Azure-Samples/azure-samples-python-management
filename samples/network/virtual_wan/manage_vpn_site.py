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
    VPN_SITE = "vpn_sitexxyyzz"
    VIRTUAL_WAN = "virtualwanxxxzz"

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

    # Create vpn site
    vpn_site = network_client.vpn_sites.begin_create_or_update(
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
              "name": "vpnSiteLink1",
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
    print("Create vpn site:\n{}".format(vpn_site))

    # Get vpn site
    vpn_site = network_client.vpn_sites.get(
        GROUP_NAME,
        VPN_SITE
    )
    print("Get vpn site:\n{}".format(vpn_site))

    # Update vpn site
    vpn_site = network_client.vpn_sites.update_tags(
        GROUP_NAME,
        VPN_SITE,
        {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    )
    print("Update vpn site:\n{}".format(vpn_site))
    
    # Delete vpn site
    vpn_site = network_client.vpn_sites.begin_delete(
        GROUP_NAME,
        VPN_SITE
    ).result()
    print("Delete vpn site.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

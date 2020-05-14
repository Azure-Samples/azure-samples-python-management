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
    AZURE_FIREWALL = "azure_firewallxxyyzz"
    VIRTUAL_WAN_NAME = "wanxxx"
    VIRTUAL_HUB_NAME = "hubxxx"
    FIREWALL_POLICY_NAME = "firewallpolicy"

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
    # Create virutal wan
    wan = network_client.virtual_wans.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_WAN_NAME,
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
        VIRTUAL_HUB_NAME,
        {
          "location": "West US",
          "tags": {
            "key1": "value1"
          },
          "virtual_wan": {
            "id": wan.id
          },
          "address_prefix": "10.168.0.0/24",
          "sku": "Basic"
        }
    ).result()

    # Create firewall policy
    network_client.firewall_policies.begin_create_or_update(
        GROUP_NAME,
        FIREWALL_POLICY_NAME,
        {
          "tags": {
            "key1": "value1"
          },
          "location": "eastus",
          "threat_intel_mode": "Alert"
        }
    ).result()
    # - end -

    # Create azure firewall
    azure_firewall = network_client.azure_firewalls.begin_create_or_update(
        GROUP_NAME,
        AZURE_FIREWALL,
        {
          "tags": {
            "key1": "value1"
          },
          "location": "West US",
          "zones": [],
          "properties": {
            "sku": {
              "name": "AZFW_Hub",
              "tier": "Standard"
            },
            "threat_intel_mode": "Alert",
            "virtual_hub": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME + ""
            },
            "firewall_policy": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/firewallPolicies/" + FIREWALL_POLICY_NAME + ""
            }
          }
        }
    ).result()
    print("Create azure firewall:\n{}".format(azure_firewall))

    # Get azure firewall
    azure_firewall = network_client.azure_firewalls.get(
        GROUP_NAME,
        AZURE_FIREWALL
    )
    print("Get azure firewall:\n{}".format(azure_firewall))

    # Update azure firewall
    azure_firewall = network_client.azure_firewalls.begin_update_tags(
        GROUP_NAME,
        AZURE_FIREWALL,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update azure firewall:\n{}".format(azure_firewall))
    
    # Delete azure firewall
    azure_firewall = network_client.azure_firewalls.begin_delete(
        GROUP_NAME,
        AZURE_FIREWALL
    ).result()
    print("Delete azure firewall.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

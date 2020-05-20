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
    NAT_GATEWAY = "nat_gatewayxxyyzz"
    PUBLIC_IP_ADDRESS = "publicipaddress"
    PUBLIC_IP_PREFIX = "publicipprefix"

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
        PUBLIC_IP_ADDRESS,
        {
            'location': "eastus",
            'public_ip_allocation_method': 'Static',
            'idle_timeout_in_minutes': 4,
            'sku': {
              'name': 'Standard'
            }
        }
    ).result()

    # Create public ip prefix
    network_client.public_ip_prefixes.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_PREFIX,
        {
          "location": "eastus",
          "prefix_length": "30",
          "sku": {
            "name": "Standard"
          }
        }
    ).result()
    # - end -

    # Create nat gateway
    nat_gateway = network_client.nat_gateways.begin_create_or_update(
        GROUP_NAME,
        NAT_GATEWAY,
        {
          "location": "eastus",
          "sku": {
            "name": "Standard"
          },
          "public_ip_addresses": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS
            }
          ],
          "public_ip_prefixes": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPPrefixes/" + PUBLIC_IP_PREFIX
            }
          ]
        }
    ).result()
    print("Create nat gateway:\n{}".format(nat_gateway))

    # Get nat gateway
    nat_gateway = network_client.nat_gateways.get(
        GROUP_NAME,
        NAT_GATEWAY
    )
    print("Get nat gateway:\n{}".format(nat_gateway))

    # Update nat gateway
    nat_gateway = network_client.nat_gateways.update_tags(
        GROUP_NAME,
        NAT_GATEWAY,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update nat gateway:\n{}".format(nat_gateway))
    
    # Delete nat gateway
    nat_gateway = network_client.nat_gateways.begin_delete(
        GROUP_NAME,
        NAT_GATEWAY
    ).result()
    print("Delete nat gateway.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

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
    LOCAL_NETWORK_GATEWAY = "local_network_gatewayxxyyzz"

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

    # Create local network gateway
    local_network_gateway = network_client.local_network_gateways.begin_create_or_update(
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
    print("Create local network gateway:\n{}".format(local_network_gateway))

    # Get local network gateway
    local_network_gateway = network_client.local_network_gateways.get(
        GROUP_NAME,
        LOCAL_NETWORK_GATEWAY
    )
    print("Get local network gateway:\n{}".format(local_network_gateway))

    # Update local network gateway
    local_network_gateway = network_client.local_network_gateways.update_tags(
        GROUP_NAME,
        LOCAL_NETWORK_GATEWAY,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update local network gateway:\n{}".format(local_network_gateway))
    
    # Delete local network gateway
    local_network_gateway = network_client.local_network_gateways.begin_delete(
        GROUP_NAME,
        LOCAL_NETWORK_GATEWAY
    ).result()
    print("Delete local network gateway.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

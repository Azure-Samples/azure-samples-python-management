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
    VIRTUAL_NETWORK_PEERING = "virtual_network_peeringxxyyzz"
    VIRTUAL_NETWORK_NAME = "virtualnetwork"
    SUBNET = "subnetxxx"
    REMOTE_NETWORK_NAME = "remotenetworkxxx"
    REMOTE_SUBNET = "remotesubnetxxx"

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

    # Create remote network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        REMOTE_NETWORK_NAME,
        {
          "address_space": {
            "address_prefixes": [
              "10.2.0.0/16"
            ]
          },
          "location": "eastus"
        }
    ).result()

    # Create subnet
    network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        REMOTE_NETWORK_NAME,
        REMOTE_SUBNET,
        {
          "address_prefix": "10.2.0.0/24"
        }
    ).result()
    # - end -

    # Create virtual network peering
    virtual_network_peering = network_client.virtual_network_peerings.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        VIRTUAL_NETWORK_PEERING,
        {
          "allow_virtual_network_access": True,
          "allow_forwarded_traffic": True,
          "allow_gateway_transit": False,
          "use_remote_gateways": False,
          "remote_virtual_network": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + REMOTE_NETWORK_NAME + ""
          }
        }
    ).result()
    print("Create virtual network peering:\n{}".format(virtual_network_peering))

    # Get virtual network peering
    virtual_network_peering = network_client.virtual_network_peerings.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        VIRTUAL_NETWORK_PEERING
    )
    print("Get virtual network peering:\n{}".format(virtual_network_peering))

    # Delete virtual network peering
    virtual_network_peering = network_client.virtual_network_peerings.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        VIRTUAL_NETWORK_PEERING
    ).result()
    print("Delete virtual network peering.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

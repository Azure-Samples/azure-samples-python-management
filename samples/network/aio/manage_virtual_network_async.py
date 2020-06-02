# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.network.aio import NetworkManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_NETWORK_NAME = "virtualnetwork"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create virtual network
    async_poller = await network_client.virtual_networks.begin_create_or_update(
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
    )
    network = await async_poller.result()
    print("Create virtual network:\n{}".format(network))

    # Get virtual network
    network = await network_client.virtual_networks.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME
    )
    print("Get virtual network:\n{}".format(network))

    # List virtual network (List operation will return asyncList)
    networks = list()
    async for net in network_client.virtual_networks.list(GROUP_NAME):
        networks.append(net)
    print("List virtual networks:\n{}".format(networks))

    # Update virtual network tags
    network = await network_client.virtual_networks.update_tags(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update virtual network tags:\n{}".format(network))

    # Delete virtual network
    async_poller = await network_client.virtual_networks.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME
    )
    await async_poller.result()
    print("Delete virtual network.\n")

    # Delete Group
    async_poller = await resource_client.resource_groups.begin_delete(
        GROUP_NAME
    )
    await async_poller.result()

    await network_client.close()
    await resource_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

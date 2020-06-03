# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.eventhub.aio import EventHubManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE_NAME = "namespacex"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    eventhub_client = EventHubManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Namespace
    async_poller = await eventhub_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "eastus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    namespace = await async_poller.result()
    print("Create Namespace:\n{}".format(namespace))

    # Get Namesapce
    namespace = await eventhub_client.namespaces.get(
        GROUP_NAME,
        NAMESPACE_NAME
    )
    print("Get Namespace:\n{}".format(namespace))

    # List Namespace (List operation will return asyncList)
    namespaces = list()
    async for n in eventhub_client.namespaces.list_by_resource_group(GROUP_NAME):
        namespaces.append(n)
    print("List Namespace:\n{}".format(namespaces))


    # Update Namespace
    namespace = await eventhub_client.namespaces.update(
        GROUP_NAME,
        NAMESPACE_NAME,
        {
          "location": "eastus",
          "tags": {
            "tag3": "value3",
            "tag4": "value4"
          }
        }
    )
    print("Update Namespace:\n{}".format(namespace))

    await asyncio.sleep(30)

    # Delete Namespace
    async_poller = await eventhub_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE_NAME
    )
    await async_poller.result()
    print("Delete Namespace.\n")

    # Delete resource group
    async_poller = await resource_client.resource_groups.begin_delete(
        GROUP_NAME
    )
    await async_poller.result()

    # Close event loop
    await eventhub_client.close()
    await resource_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

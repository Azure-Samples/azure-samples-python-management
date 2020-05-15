# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredentials
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE_NAME = "namespacex"

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    eventhub_client = EventHubManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Namespace
    namesapce = eventhub_client.namespaces.begin_create_or_update(
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
    ).result()
    print("Create Namespace: {}".format(namesapce))

    # Get Namesapce
    namespace = eventhub_client.namespaces.get(
        GROUP_NAME,
        NAMESPACE_NAME
    )
    print("Get Namespace: {}".format(namespace))

    # Update Namespace
    namespace = eventhub_client.namespaces.update(
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
    print("Update Namespace: {}".format(namesapce))

    # Delete Namespace
    eventhub_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE_NAME
    ).result()
    print("Delete Namespace.")

    # Delete resource group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

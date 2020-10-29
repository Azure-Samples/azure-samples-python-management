# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxx"
    NAMESPACE = "namespacexxyyzz"
    QUEUE = "queuexxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    servicebus_client = ServiceBusManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create namespace
    namespace = servicebus_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
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
    # - end -

    # Create queue
    queue = servicebus_client.queues.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        QUEUE,
        {
            "enable_partitioning": True
        }
    )
    print("Create queue:\n{}".format(queue))

    # Get queue
    queue = servicebus_client.queues.get(
        GROUP_NAME,
        NAMESPACE,
        QUEUE
    )
    print("Get queue:\n{}".format(queue))

    # Delete queue
    queue = servicebus_client.queues.delete(
        GROUP_NAME,
        NAMESPACE,
        QUEUE
    )
    print("Delete queue.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

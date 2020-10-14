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
    GROUP_NAME = "testgroupx"
    NAMESPACE = "namespacexxyyzz"
    TOPIC = "topicxxyyzz"

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

    # Create topic
    topic = servicebus_client.topics.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        TOPIC,
        {
            "enable_express": True
        }
    )
    print("Create topic:\n{}".format(topic))

    # Get topic
    topic = servicebus_client.topics.get(
        GROUP_NAME,
        NAMESPACE,
        TOPIC
    )
    print("Get topic:\n{}".format(topic))

    # Delete topic
    topic = servicebus_client.topics.delete(
        GROUP_NAME,
        NAMESPACE,
        TOPIC
    )
    print("Delete topic.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

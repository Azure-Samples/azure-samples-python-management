# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT_NAME = "storageaccountxyztest"
    NAMESPACE_NAME = "namespacex"
    EVENTHUB_NAME = "eventhubx"
    CONSUMERGROUP_NAME = "consumergroup"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    eventhub_client = EventHubManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    storage_client = StorageManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create StorageAccount
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
          "sku": {
            "name": "Standard_LRS"
          },
          "kind": "StorageV2",
          "location": "eastus"
        }
    ).result()

    # Create Namespace
    eventhub_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "South Central US",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    # Create EventHub
    eventhub_client.event_hubs.create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
        EVENTHUB_NAME,
        {
          "message_retention_in_days": "4",
          "partition_count": "4",
          "status": "Active",
          "capture_description": {
            "enabled": True,
            "encoding": "Avro",
            "interval_in_seconds": "120",
            "size_limit_in_bytes": "10485763",
            "destination": {
              "name": "EventHubArchive.AzureBlockBlob",
              "storage_account_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME + "",
              "blob_container": "container",
              "archive_name_format": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
            }
          }
        }
    )

    # Create Consumer Group
    consumer_group = eventhub_client.consumer_groups.create_or_update(
        GROUP_NAME,
        NAMESPACE_NAME,
        EVENTHUB_NAME,
        CONSUMERGROUP_NAME,
        {
          "user_metadata": "New consumergroup"
        }
    )
    print("Create consumer group:\n{}".format(consumer_group))

    # Get Consumer Group
    consumer_group = eventhub_client.consumer_groups.get(
        GROUP_NAME,
        NAMESPACE_NAME,
        EVENTHUB_NAME,
        CONSUMERGROUP_NAME
    )
    print("Get consumer group:\n{}".format(consumer_group))

    # Delete Consumer Group
    eventhub_client.consumer_groups.delete(
        GROUP_NAME,
        NAMESPACE_NAME,
        EVENTHUB_NAME,
        CONSUMERGROUP_NAME
    )
    print("Delete consumer group.")

    # Delete EventHub
    eventhub_client.event_hubs.delete(
        GROUP_NAME,
        NAMESPACE_NAME,
        EVENTHUB_NAME
    )

    # Delete Namespace
    eventhub_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE_NAME
    ).result()

    # Delete StorageAccount
    storage_client.storage_accounts.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME
    )

    # Delete resource group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

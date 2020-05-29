# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.storage.aio import StorageManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT = "storageaccountxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create storage account
    storage_account = await storage_client.storage_accounts.create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
          "sku": {
            "name": "Standard_GRS"
          },
          "kind": "StorageV2",
          "location": "eastus",
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          },
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    )
    print("Create storage account:\n{}".format(storage_account))

    # Get storage account
    storage_account = await storage_client.storage_accounts.get_properties(
        GROUP_NAME,
        STORAGE_ACCOUNT
    )
    print("Get storage account:\n{}".format(storage_account))

    # List storage account (List operation will return asyncList)
    storage_accounts = list()
    async for ac in storage_client.storage_accounts.list():
        storage_accounts.append(ac)
    print("List storage accounts:\n{}".format(storage_accounts))

    # Update storage account
    storage_account = await storage_client.storage_accounts.update(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
          "network_acls": {
            "default_action": "Allow"
          },
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          }
        }
    )
    print("Update storage account:\n{}".format(storage_account))
    
    # Delete storage account
    storage_account = await storage_client.storage_accounts.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT
    )
    print("Delete storage account.\n")

    # Delete Group
    await resource_client.resource_groups.delete(
        GROUP_NAME
    )

    await storage_client.close()
    await resource_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

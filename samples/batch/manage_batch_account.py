# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.batch import BatchManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    BATCH_ACCOUNT = "batchaccountxxyyzz"
    STORAGE_ACCOUNT = "storageaccountxxy"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    batch_client = BatchManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create storage account
    storage_account = storage_client.storage_accounts.begin_create(
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
    ).result()
    print("Create storage account:\n{}".format(storage_account))
    # - end -

    # Create batch account
    batch_account = batch_client.batch_account.begin_create(
        GROUP_NAME,
        BATCH_ACCOUNT,
        {
            "location": "eastus",
            "auto_storage": {
                "storage_account_id": storage_account.id
            }
        }
    ).result()
    print("Create batch account:\n{}".format(batch_account))

    # Get batch account
    batch_account = batch_client.batch_account.get(
        GROUP_NAME,
        BATCH_ACCOUNT
    )
    print("Get batch account:\n{}".format(batch_account))

    # Update batch account
    batch_account = batch_client.batch_account.update(
        GROUP_NAME,
        BATCH_ACCOUNT,
        {
            "location": "eastus",
            "auto_storage": {
                "storage_account_id": storage_account.id
            }
        }
    )
    print("Update batch account:\n{}".format(batch_account))
    
    # Delete batch account
    batch_account = batch_client.batch_account.begin_delete(
        GROUP_NAME,
        BATCH_ACCOUNT
    ).result()
    print("Delete batch account.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

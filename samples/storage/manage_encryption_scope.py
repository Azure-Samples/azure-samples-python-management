# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT = "storageaccountxxyzz"
    ENCRYPTION_SCOPE = "encryptionscopexxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create storage account
    storage_client.storage_accounts.begin_create(
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
    # - end -

    # Create encryption scope
    encryption_scope = storage_client.encryption_scopes.put(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        ENCRYPTION_SCOPE,
        {
          "source": "Microsoft.Storage",
          "state": "Enabled"
        }
    )
    print("Create encryption scope:\n{}".format(encryption_scope))

    # Get encryption scope
    encryption_scope = storage_client.encryption_scopes.get(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        ENCRYPTION_SCOPE
    )
    print("Get encryption scope:\n{}".format(encryption_scope))

    # Update encryption scope
    encryption_scope = storage_client.encryption_scopes.patch(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        ENCRYPTION_SCOPE,
        {
          "source": "Microsoft.Storage",
          "state": "Enabled"
        }
    )
    print("Update encryption scope:\n{}".format(encryption_scope))
    
    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

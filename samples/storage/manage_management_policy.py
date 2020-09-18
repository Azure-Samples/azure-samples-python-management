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
    STORAGE_ACCOUNT = "storageaccountxxxyy"
    POLICY_NAME = "default"

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
          "kind": "StorageV2",  # Storage v2 support policy
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

    # Create management policy
    management_policy = storage_client.management_policies.create_or_update(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        POLICY_NAME,
        {
          "policy": {
            "rules": [
              {
                "enabled": True,
                "name": "olcmtest",
                "type": "Lifecycle",
                "definition": {
                  "filters": {
                    "blob_types": [
                      "blockBlob"
                    ],
                    "prefix_match": [
                      "olcmtestcontainer"
                    ]
                  },
                  "actions": {
                    "base_blob": {
                      "tier_to_cool": {
                        "days_after_modification_greater_than": "30"
                      },
                      "tier_to_archive": {
                        "days_after_modification_greater_than": "90"
                      },
                      "delete": {
                        "days_after_modification_greater_than": "1000"
                      }
                    },
                    "snapshot": {
                      "delete": {
                        "days_after_creation_greater_than": "30"
                      }
                    }
                  }
                }
              }
            ]
          }
        }
    )
    print("Create management policy:\n{}".format(management_policy))

    # Get management policy
    management_policy = storage_client.management_policies.get(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        POLICY_NAME
    )
    print("Get management policy:\n{}".format(management_policy))

    # Delete management policy
    management_policy = storage_client.management_policies.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        POLICY_NAME
    )
    print("Delete management policy.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

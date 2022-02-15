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
    STORAGE_ACCOUNT = "storageaccountxxyzzzx"
    ACCOUNT = "accountxxyzxx"
    POOL = "poolxxyyzz"

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
    
    # Create account
    account = batch_client.batch_account.begin_create(
        GROUP_NAME,
        ACCOUNT,
        {
            "location": "eastus",
            "auto_storage": {
                "storage_account_id": storage_account.id
            }
        }
    ).result()
    print("Create batch account:\n{}".format(account))
    # - end -

    # Create pool
    pool = batch_client.pool.create(
        GROUP_NAME,
        ACCOUNT,
        POOL,
        {
            "properties": {
            "vmSize": "STANDARD_D4",
            "deploymentConfiguration": {
                "virtualMachineConfiguration": {
                    "imageReference": {
                        "publisher": "Canonical",
                        "offer": "UbuntuServer",
                        "sku": "18.04-LTS",
                        "version": "latest"
                    },
                    "nodeAgentSkuId": "batch.node.ubuntu 18.04"
                }
            },
            "scaleSettings": {
                "autoScale": {
                    "formula": "$TargetDedicatedNodes=1",
                    "evaluationInterval": "PT5M"
                }
            }
        },

        #If you want to create your pool with identity, please cancel the notes below.Remember to fill in your own identity name on "your identity name"
            
        # "identity": {
        #     "type": "UserAssigned",
        #     "userAssignedIdentities": {
        #         "/subscriptions/"+SUBSCRIPTION_ID+"/resourceGroups/"+GROUP_NAME+"/providers/Microsoft.ManagedIdentity/userAssignedIdentities/"+"Your Identity Name": {}
        #     }
        #
        # }
        }
    )
    print("Create pool:\n{}".format(pool))

    # Get pool
    pool = batch_client.pool.get(
        GROUP_NAME,
        ACCOUNT,
        POOL
    )
    print("Get pool:\n{}".format(pool))

    # Update pool
    pool = batch_client.pool.update(
        GROUP_NAME,
        ACCOUNT,
        POOL,
        {
            "scale_settings": {
                "auto_scale": {
                    "formula": "$TargetDedicatedNodes=0"
                }
            }
        }
    )
    print("Update pool:\n{}".format(pool))
    
    # Delete pool
    pool = batch_client.pool.begin_delete(
        GROUP_NAME,
        ACCOUNT,
        POOL
    ).result()
    print("Delete pool.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

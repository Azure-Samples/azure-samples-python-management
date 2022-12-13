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
    STORAGE_ACCOUNT = "storageaccountxxyyzz"

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

    # Create storage account for public access and with IP restrictions
    storage_account = storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            # "publicNetworkAccess": "Disable",
            "publicNetworkAccess": "Enabled",
            "kind": "StorageV2",
            "location": "eastus",
            "encryption": {
                "services": {
                    "file": {
                        "keyType": "Account",
                        "enabled": "true"
                    },
                    "blob": {
                        "keyType": "Account",
                        "enabled": "true"
                    }
                },
                "requireInfrastructureEncryption": "false",
                "keySource": "Microsoft.Storage"
            },
            "tags": {
                "key1": "value1",
                "key2": "value2"
            },
            "networkAcls": {
                "ipRules": [
                    {
                        "ip_address_or_range": "x.y.z.z",
                        "action": "allow"
                    }
                ],
                "virtual_network_rules": [],
                "bypass": "AzureServices",
                "defaultAction": "Allow",
            },
            "enable_https_traffic_only": True,
        }
    ).result()
    print("Create storage account:\n{}".format(storage_account))

    # Delete storage account
    storage_client.storage_accounts.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT
    )
    print("Delete storage account.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

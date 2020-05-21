# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredentials
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    LOGPROFILE_NAME = "logprofilexx"
    STORAGE_ACCOUNT_NAME = "storageaccountxxy"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Storage
    storage_account = storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            "sku":{
                "name": "Standard_LRS"
            },
            "kind": "Storage",
            "location": "eastus",
            "enable_https_traffic_only": True
        }
    ).result()

    # Create log profile
    log_profile = monitor_client.log_profiles.create_or_update(
        LOGPROFILE_NAME,
        {
          "location": "",
          "locations": [
            "global"
          ],
          "categories": [
            "Write",
            "Delete",
            "Action"
          ],
          "retention_policy": {
            "enabled": True,
            "days": "3"
          },
          "storage_account_id": storage_account.id,
        }
    )
    print("Create log profile:\n{}".format(log_profile))

    # Get log profile
    log_profile = monitor_client.log_profiles.delete(LOGPROFILE_NAME)
    print("Get log profile:\n{}".format(log_profile))

    # Delete log profile
    monitor_client.log_profiles.delete(LOGPROFILE_NAME)
    print("Delete log profile.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

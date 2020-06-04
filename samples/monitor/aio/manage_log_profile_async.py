# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.monitor.aio import MonitorClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.storage.aio import StorageManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    LOGPROFILE_NAME = "logprofilexx"
    STORAGE_ACCOUNT_NAME = "storageaccountxxy"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
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

    # Create Storage
    async_poller = await storage_client.storage_accounts.begin_create(
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
    )
    storage_account = await async_poller.result()

    # Create log profile
    log_profile = await monitor_client.log_profiles.create_or_update(
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

    # Need wait seconds
    await asyncio.sleep(20)

    # Get log profile
    log_profile = await monitor_client.log_profiles.get(LOGPROFILE_NAME)
    print("Get log profile:\n{}".format(log_profile))

    # List log profile (List operation will return asyncList)
    log_profiles = list()
    async for log in monitor_client.log_profiles.list():
        log_profiles.append(log)
    print("List log profiles:\n{}".format(log_profiles))

    # Delete log profile
    await monitor_client.log_profiles.delete(LOGPROFILE_NAME)
    print("Delete log profile.\n")

    # Delete Group
    async_poller = await resource_client.resource_groups.begin_delete(
        GROUP_NAME
    )
    await async_poller.result()

    # [Warning] All clients and credentials need to be closed.
    # link: https://github.com/Azure/azure-sdk-for-python/issues/8990
    await monitor_client.close()
    await resource_client.close()
    await storage_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

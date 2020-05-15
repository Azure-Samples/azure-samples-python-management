# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredentials
from azure.mgmt.resource import ManagementLockClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    LOCK_NAME = "locktestx"

    # Create client
    lock_client = ManagementLockClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create resource lock
    lock = lock_client.management_locks.create_or_update_at_resource_group_level(
        GROUP_NAME,
        LOCK_NAME,
        {
            "level": "CanNotDelete"
        }
    )
    print("Create lock: {}".format(lock))

    # Get lock
    lock = lock_client.management_locks.get_at_resource_group_level(
        GROUP_NAME,
        LOCK_NAME
    )
    print("Get lock: {}".format(lock))

    # Delete lock
    lock_client.management_locks.delete_at_resource_group_level(
        GROUP_NAME,
        LOCK_NAME
    )
    print("Delete lock.")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

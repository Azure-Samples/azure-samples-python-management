# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    DISK = "diskxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create disk
    disk = compute_client.disks.begin_create_or_update(
        GROUP_NAME,
        DISK,
        {
            "location": "eastus",
            "creation_data": {
                "create_option": "Empty"
            },
            "disk_size_gb": "200"
        }
    ).result()
    print("Create disk:\n{}".format(disk))

    # Get disk
    disk = compute_client.disks.get(
        GROUP_NAME,
        DISK
    )
    print("Get disk:\n{}".format(disk))

    # Update disk
    disk = compute_client.disks.begin_update(
        GROUP_NAME,
        DISK,
        {
            "disk_size_gb": "200"
        }
    ).result()
    print("Update disk:\n{}".format(disk))
    
    # Delete disk
    disk = compute_client.disks.begin_delete(
        GROUP_NAME,
        DISK
    ).result()
    print("Delete disk.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

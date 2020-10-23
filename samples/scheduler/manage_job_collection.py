# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.scheduler import SchedulerManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    JOB_COLLECTION = "jobcollectionxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    scheduler_client = SchedulerManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create job collection
    job_collection = scheduler_client.job_collections.create_or_update(
        GROUP_NAME,
        JOB_COLLECTION,
        {
            "location": "eastus",
            "properties": {
                "sku": {
                    "name": "Free"
                }
            }
        }
    )
    print("Create job collection:\n{}".format(job_collection))

    # Get job collection
    job_collection = scheduler_client.job_collections.get(
        GROUP_NAME,
        JOB_COLLECTION
    )
    print("Get job collection:\n{}".format(job_collection))

    # Delete job collection
    job_collection = scheduler_client.job_collections.begin_delete(
        GROUP_NAME,
        JOB_COLLECTION
    ).result()
    print("Delete job collection.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

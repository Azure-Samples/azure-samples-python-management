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
    AVAILABILITY_SET_NAME = "availabilityset"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
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

    # Create availability set
    availability_set = compute_client.availability_sets.create_or_update(
        GROUP_NAME,
        AVAILABILITY_SET_NAME,
        {
          "location": "eastus",
          "platform_fault_domain_count": "2",
          "platform_update_domain_count": "20"
        }
    )
    print("Create availability set:\n{}".format(availability_set))

    # Get availability set
    availability_set = compute_client.availability_sets.get(
        GROUP_NAME,
        AVAILABILITY_SET_NAME
    )
    print("Get availability set:\n{}".format(availability_set))

    # Update availability set
    availability_set = compute_client.availability_sets.update(
        GROUP_NAME,
        AVAILABILITY_SET_NAME,
        {
          "platform_fault_domain_count": "2",
          "platform_update_domain_count": "20"
        }
    )
    print("Update availability set:\n{}".format(availability_set))

    # Delete availability set
    compute_client.availability_sets.delete(
        GROUP_NAME,
        AVAILABILITY_SET_NAME
    )
    print("Delete availability set.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

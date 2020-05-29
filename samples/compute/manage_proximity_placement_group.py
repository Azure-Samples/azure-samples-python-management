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
    PROXIMITY_PLACEMENT_GROUP_NAME = "proximityplacementgroup"

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

    # Create proximity placement group
    proximity_placement_group = compute_client.proximity_placement_groups.create_or_update(
        GROUP_NAME,
        PROXIMITY_PLACEMENT_GROUP_NAME,
        {
          "location": "eastus",
          "proximity_placement_group_type": "Standard"
        }
    )
    print("Create proximity placement group:\n{}".format(proximity_placement_group))

    # Get proximity placement group
    proximity_placement_group = compute_client.proximity_placement_groups.get(
        GROUP_NAME,
        PROXIMITY_PLACEMENT_GROUP_NAME
    )
    print("Get proximity placement group:\n{}".format(proximity_placement_group))

    # Update proximity placement group
    proximity_placement_group = compute_client.proximity_placement_groups.update(
        GROUP_NAME,
        PROXIMITY_PLACEMENT_GROUP_NAME,
        {
          "location": "eastus",
          "proximity_placement_group_type": "Standard"
        }
    )
    print("Update proximity placement group:\n{}".format(proximity_placement_group))

    # Delete proximity placement group
    compute_client.proximity_placement_groups.delete(
        GROUP_NAME,
        PROXIMITY_PLACEMENT_GROUP_NAME
    )
    print("Delete proximity placement group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

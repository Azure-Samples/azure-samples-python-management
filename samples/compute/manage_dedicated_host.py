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
    HOST_GROUP_NAME = "hostgroupx"
    HOST_NAME = "hostx"

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

    # Create dedicated host group
    host_group = compute_client.dedicated_host_groups.create_or_update(
        GROUP_NAME,
        HOST_GROUP_NAME,
        {
          "location": "eastus",
          "tags": {
            "department": "finance"
          },
          "zones": [
            "1"
          ],
          "platform_fault_domain_count": "3"
        }
    )
    print("Create dedicated host group:\n{}".format(host_group))

    # Create dedicated host
    host = compute_client.dedicated_hosts.begin_create_or_update(
        GROUP_NAME,
        HOST_GROUP_NAME,
        HOST_NAME,
        {
          "location": "eastus",
          "tags": {
            "department": "HR"
          },
          "platform_fault_domain": "1",
          "sku": {
            "name": "DSv3-Type1"
          }
        }
    ).result()
    print("Create dedicated host:\n{}".format(host))

    # Get dedicated host group
    host_group = compute_client.dedicated_host_groups.get(
        GROUP_NAME,
        HOST_GROUP_NAME
    )
    print("Get dedicated host group:\n{}".format(host_group))

    # Get dedicated host
    host = compute_client.dedicated_hosts.get(
        GROUP_NAME,
        HOST_GROUP_NAME,
        HOST_NAME
    )
    print("Get dedicated host:\n{}".format(host))

    # Update dedicated host group
    host_group = compute_client.dedicated_host_groups.update(
        GROUP_NAME,
        HOST_GROUP_NAME,
        {
          "tags": {
            "department": "finance"
          },
          "platform_fault_domain_count": "3"
        }
    )
    print("Update dedicated host group:\n{}".format(host_group))

    # Update dedicated host
    host = compute_client.dedicated_hosts.begin_update(
        GROUP_NAME,
        HOST_GROUP_NAME,
        HOST_NAME,
        {
          "tags": {
            "department": "HR"
          }
        }
    ).result()
    print("Update dedicated host:\n{}".format(host))

    # Delete dedicated host
    compute_client.dedicated_hosts.begin_delete(
        GROUP_NAME,
        HOST_GROUP_NAME,
        HOST_NAME
    ).result()
    print("Delete dedicated host.\n")

    # Delete dedicated host group
    compute_client.dedicated_host_groups.delete(
        GROUP_NAME,
        HOST_GROUP_NAME
    )
    print("Delete dedicated host group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

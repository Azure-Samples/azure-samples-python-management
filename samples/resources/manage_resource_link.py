# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ManagementLinkClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RESOURCE_1 = "resource1"
    RESOURCE_2 = "resource2"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    link_client = ManagementLinkClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create resource 1
    resource_1 = resource_client.resources.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_1,
        parameters={'location': "eastus"},
        api_version='2019-07-01'
    ).result()

    # Create resource 2
    resource_2 = resource_client.resources.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_2,
        parameters={'location': "eastus"},
        api_version='2019-07-01'
    ).result()

    # Create link
    link = link_client.resource_links.create_or_update(
        resource_1.id + "/providers/Microsoft.Resources/links/myLink",
        {
            "properties": {
                "target_id": resource_2.id,
                "notes": "Testing links"
            }
        }
    )
    print("Create link:\n{}".format(link))

    # Get link
    link = link_client.resource_links.get(link.id)
    print("Get link:\n{}".format(link))

    # Delete link
    link_client.resource_links.delete(
        link.id
    )
    print("Delete link.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

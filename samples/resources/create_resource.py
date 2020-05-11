# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RESOURCE_NAME = "pytestresource"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Check resource existence
    check_result = resource_client.resources.check_existence(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_NAME,
        api_version="2019-10-01"
    )
    print("Check resource existence:\n{}".format(check_result))

    # Create resource
    resource = resource_client.resources.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_NAME,
        parameters={'location': "eastus"},
        api_version="2019-07-01"
    ).result()
    print("Create resource:\n{}".format(resource))

    # Get resource
    resource = resource_client.resources.get(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_NAME,
        api_version="2019-07-01"
    )
    print("Get resource:\n{}".format(resource))

    # Update resource
    resource = resource_client.resources.begin_update(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_NAME,
        parameters={'tags': {"tag1": "value1"}},
        api_version="2019-07-01"
    ).result()
    print("Update resource:\n{}".format(resource))

    # Delete resource
    resource_client.resources.begin_delete(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Compute",
        parent_resource_path="",
        resource_type="availabilitySets",
        resource_name=RESOURCE_NAME,
        api_version="2019-07-01"
    ).result()
    print("Delete resource.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

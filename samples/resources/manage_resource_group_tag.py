# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup, ResourceGroupPatchable
from azure.core.serialization import NULL as AzureCoreNull

import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout)

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxx"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        logging_enable=True
    )

    # Create resource group
    resource_group = resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        parameters=ResourceGroup(location="eastus")
    )
    print("Create resource group:\n{}".format(resource_group.serialize()))

    # Update resource group
    resource_group = resource_client.resource_groups.update(
        GROUP_NAME,
        parameters=ResourceGroupPatchable(tags={"hello": "world"})
    )
    print("Update resource group:\n{}".format(resource_group.serialize()))

    resource_group = resource_client.resource_groups.update(
        GROUP_NAME,
        parameters=ResourceGroupPatchable(tags=None)
    )
    print("Update resource group:\n{}".format(resource_group.serialize()))

    resource_group = resource_client.resource_groups.update(
        GROUP_NAME,
        parameters=ResourceGroupPatchable(tags=AzureCoreNull)
    )
    print("Update resource group:\n{}".format(resource_group.serialize()))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()
    print("Delete resource group.\n")


if __name__ == "__main__":
    main()

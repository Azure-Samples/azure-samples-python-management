# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    REGISTRIES = "registriesxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    registry_client = ContainerRegistryManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create registries
    registries = registry_client.registries.begin_create(
        GROUP_NAME,
        REGISTRIES,
        {
          "location": "eastus",
          "tags": {
            "key": "value"
          },
          "sku": {
            "name": "Standard"
          },
          "admin_user_enabled": True
        }
    ).result()
    print("Create registries:\n{}".format(registries))

    # Get registries
    registries = registry_client.registries.get(
        GROUP_NAME,
        REGISTRIES
    )
    print("Get registries:\n{}".format(registries))

    # Update registries
    registries = registry_client.registries.begin_update(
        GROUP_NAME,
        REGISTRIES,
        {
          "tags": {
            "key": "value"
          },
          "sku": {
            "name": "Standard"
          },
          "admin_user_enabled": True
        }
    ).result()
    print("Update registries:\n{}".format(registries))
    
    # Delete registries
    registries = registry_client.registries.begin_delete(
        GROUP_NAME,
        REGISTRIES
    ).result()
    print("Delete registries.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

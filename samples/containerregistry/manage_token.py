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
    TOKEN = "tokenxxyyzz"
    REGISTRIES = "registriesxxyyzz"
    SCOPE_MAP = "scopemapxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    containerregistry_client = ContainerRegistryManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        api_version="2019-12-01-preview"
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    registries = containerregistry_client.registries.begin_create(
        GROUP_NAME,
        REGISTRIES,
        {
          "location": "eastus",
          "tags": {
            "key": "value"
          },
          "sku": {
            "name": "Premium"
          },
          "admin_user_enabled": True
        }
    ).result()
    scope_map = containerregistry_client.scope_maps.begin_create(
        GROUP_NAME,
        REGISTRIES,
        SCOPE_MAP,
        {
          "description": "Developer Scopes",
          "actions": [
            "repositories/foo/content/read",
            "repositories/foo/content/delete"
          ]
        }
    ).result()
    # - end -

    # Create token
    token = containerregistry_client.tokens.begin_create(
        GROUP_NAME,
        REGISTRIES,
        TOKEN,
        {
          "scope_map_id": scope_map.id,
          "status": "enabled",
        }
    ).result()
    print("Create token:\n{}".format(token))

    # Get token
    token = containerregistry_client.tokens.get(
        GROUP_NAME,
        REGISTRIES,
        TOKEN
    )
    print("Get token:\n{}".format(token))

    # Update token
    token = containerregistry_client.tokens.begin_update(
        GROUP_NAME,
        REGISTRIES,
        TOKEN,
        {
          "scope_map_id": scope_map.id
        }
    ).result()
    print("Update token:\n{}".format(token))
    
    # Delete token
    token = containerregistry_client.tokens.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        TOKEN
    ).result()
    print("Delete token.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

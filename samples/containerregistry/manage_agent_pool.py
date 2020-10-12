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
    AGENT_POOL = "agentpoolxxyyzz"
    REGISTRIES = "registriesxxyyzz"

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
    # - end -

    # Create agent pool
    agent_pool = containerregistry_client.agent_pools.begin_create(
        GROUP_NAME,
        REGISTRIES,
        AGENT_POOL,
        {
          "location": "eastus",
          "tags": {
            "key": "value"
          },
          "count": "1",
          "tier": "S1",
          "os": "Linux"
        }
    ).result()
    print("Create agent pool:\n{}".format(agent_pool))

    # Get agent pool
    agent_pool = containerregistry_client.agent_pools.get(
        GROUP_NAME,
        REGISTRIES,
        AGENT_POOL
    )
    print("Get agent pool:\n{}".format(agent_pool))

    # Update agent pool
    agent_pool = containerregistry_client.agent_pools.begin_update(
        GROUP_NAME,
        REGISTRIES,
        AGENT_POOL,
        {
            "count": "1"
        }
    ).result()
    print("Update agent pool:\n{}".format(agent_pool))
    
    # Delete agent pool
    agent_pool = containerregistry_client.agent_pools.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        AGENT_POOL
    ).result()
    print("Delete agent pool.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

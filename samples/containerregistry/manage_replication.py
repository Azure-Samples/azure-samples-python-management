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
    REPLICATION = "replicationxxyyzz"
    REGISTRIES = "registriesxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    containerregistry_client = ContainerRegistryManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create registries
    registries = containerregistry_client.registries.begin_create(
        GROUP_NAME,
        REGISTRIES,
        {
          "location": "eastus",
          "tags": {
            "key": "value"
          },
          "sku": {
            "name": "Premium",  # replication needs Premium sku
          },
          "admin_user_enabled": True
        }
    ).result()
    # - end -

    # Create replication
    replication = containerregistry_client.replications.begin_create(
        GROUP_NAME,
        REGISTRIES,
        REPLICATION,
        {
          "location": "westus",
          "tags": {
            "key": "value"
          }
        }
    ).result()
    print("Create replication:\n{}".format(replication))

    # Get replication
    replication = containerregistry_client.replications.get(
        GROUP_NAME,
        REGISTRIES,
        REPLICATION
    )
    print("Get replication:\n{}".format(replication))

    # Update replication
    replication = containerregistry_client.replications.begin_update(
        GROUP_NAME,
        REGISTRIES,
        REPLICATION,
        {
          "tags": {
            "key": "value"
          }
        }
    ).result()
    print("Update replication:\n{}".format(replication))
    
    # Delete replication
    replication = containerregistry_client.replications.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        REPLICATION
    ).result()
    print("Delete replication.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

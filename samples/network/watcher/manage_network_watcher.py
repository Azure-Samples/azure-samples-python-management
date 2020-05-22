# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NETWORK_WATCHER = "network_watcherxxyyzz"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create network watcher
    network_watcher = network_client.network_watchers.create_or_update(
        GROUP_NAME,
        NETWORK_WATCHER,
        {
          "location": "eastus"
        }
    )
    print("Create network watcher:\n{}".format(network_watcher))

    # Get network watcher
    network_watcher = network_client.network_watchers.get(
        GROUP_NAME,
        NETWORK_WATCHER
    )
    print("Get network watcher:\n{}".format(network_watcher))

    # Update network watcher
    network_watcher = network_client.network_watchers.update_tags(
        GROUP_NAME,
        NETWORK_WATCHER,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update network watcher:\n{}".format(network_watcher))
    
    # Delete network watcher
    network_watcher = network_client.network_watchers.begin_delete(
        GROUP_NAME,
        NETWORK_WATCHER
    ).result()
    print("Delete network watcher.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

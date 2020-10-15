# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    CONTAINER_GROUP = "container_groupxxyyzz"
    CONTAINER_NAME = "my-container"  # must match the regex '[a-z0-9]([-a-z0-9]*[a-z0-9])?'

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    containerinstance_client = ContainerInstanceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create container group
    container_group = containerinstance_client.container_groups.begin_create_or_update(
        GROUP_NAME,
        CONTAINER_GROUP,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
          },
          "containers": [
            {
              "name": CONTAINER_NAME,
              "command": [],
              "environment_variables": [],
              "image": "nginx",
              "ports": [
                {
                  "port": "80"
                }
              ],
              "resources": {
                "requests": {
                  "cpu": "1",
                  "memory_in_gb": "1.5",
                  "gpu": {
                    "count": "1",
                    "sku": "K80"
                  }
                }
              },
              "volume_mounts": [
                {
                  "name": "empty-volume",
                  "mount_path": "/mnt/mydir"
                }
              ]
            }
          ],
          "diagnostics": {
            "log_analytics": {
              "workspace_id": "workspaceid",
              "workspace_key": "workspaceKey"
            }
          },
          "os_type": "Linux",
          "restart_policy": "OnFailure",
          "volumes": [
            {
              "name": "empty-volume",
              "empty_dir": {}
            }
          ]
        }
    ).result()
    print("Create container group:\n{}".format(container_group))

    # Get container group
    container_group = containerinstance_client.container_groups.get(
        GROUP_NAME,
        CONTAINER_GROUP
    )
    print("Get container group:\n{}".format(container_group))

    # Update container group
    container_group = containerinstance_client.container_groups.update(
        GROUP_NAME,
        CONTAINER_GROUP,
        {
          "tags": {
            "tag1key": "tag1Value",
            "tag2key": "tag2Value"
          }
        }
    )
    print("Update container group:\n{}".format(container_group))

    # Container exec
    result = containerinstance_client.containers.execute_command(
        GROUP_NAME,
        CONTAINER_GROUP,
        CONTAINER_NAME,
        {
          "command": "/bin/bash",
          "terminal_size": {
            "rows": "12",
            "cols": "12"
          }
        }
    )
    print("Container exec:\n{}".format(result))
    
    # Delete container group
    container_group = containerinstance_client.container_groups.begin_delete(
        GROUP_NAME,
        CONTAINER_GROUP
    ).result()
    print("Delete container group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

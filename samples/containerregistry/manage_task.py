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
    TASK = "taskxxyyzz"
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

    # Create task
    task = containerregistry_client.tasks.begin_create(
        GROUP_NAME,
        REGISTRIES,
        TASK,
        {
          "location": "eastus",
          "tags": {
            "testkey": "value"
          },
          "status": "Enabled",
          "platform": {
            "os": "Linux",
            "architecture": "amd64"
          },
          "agent_configuration": {
            "cpu": "2"
          },
          "step": {
            "type": "Docker",
            "context_path": "https://github.com/SteveLasker/node-helloworld",
            "image_names": [
                "testtask:v1"
            ],
            "docker_file_path": "DockerFile",
            "is_push_enabled": True,
            "no_cache": False,
          },
          "trigger": {
            "base_image_trigger": {
              "name": "myBaseImageTrigger",
              "base_image_trigger_type": "Runtime",
              "update_trigger_payload_type": "Default",
              "status": "Enabled"
            }
          }
        }
    ).result()
    print("Create task:\n{}".format(task))

    # Get task
    task = containerregistry_client.tasks.get(
        GROUP_NAME,
        REGISTRIES,
        TASK
    )
    print("Get task:\n{}".format(task))

    # Update task
    task = containerregistry_client.tasks.begin_update(
        GROUP_NAME,
        REGISTRIES,
        TASK,
        {
          "location": "eastus",
          "tags": {
            "testkey": "value"
          },
          "status": "Enabled",
          "platform": {
            "os": "Linux",
            "architecture": "amd64"
          },
          "agent_configuration": {
            "cpu": "2"
          },
          "step": {
            "type": "Docker",
            "context_path": "https://github.com/SteveLasker/node-helloworld",
            "image_names": [
                "testtask:v1"
            ],
            "docker_file_path": "DockerFile",
            "is_push_enabled": True,
            "no_cache": False,
          },
          "trigger": {
            "base_image_trigger": {
              "name": "myBaseImageTrigger",
              "base_image_trigger_type": "Runtime",
              "update_trigger_payload_type": "Default",
              "status": "Enabled"
            }
          }
        }
    ).result()
    print("Update task:\n{}".format(task))
    
    # Delete task
    task = containerregistry_client.tasks.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        TASK
    ).result()
    print("Delete task.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

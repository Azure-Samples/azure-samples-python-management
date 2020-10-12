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
    TASK_RUN = "taskrunxxyyzz"
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

    # Create task run
    task_run = containerregistry_client.task_runs.begin_create(
        GROUP_NAME,
        REGISTRIES,
        TASK_RUN,
        {
          "force_update_tag": "test",
          "run_request": {
            "type": "DockerBuildRequest",
            "image_names": ["testtaskrun:v1"],
            "is_push_enabled": True,
            "no_cache": False,
            "docker_file_path": "Dockerfile",
            "platform": {
              "os": "linux",
              "architecture": "amd64"
            },
            "source_location": "https://github.com/Azure-Samples/acr-build-helloworld-node.git",
            "is_archive_enabled": True
          }
        }
    ).result()
    print("Create task run:\n{}".format(task_run))

    # Get task run
    task_run = containerregistry_client.task_runs.get(
        GROUP_NAME,
        REGISTRIES,
        TASK_RUN
    )
    print("Get task run:\n{}".format(task_run))

    # Update task run
    task_run = containerregistry_client.task_runs.begin_update(
        GROUP_NAME,
        REGISTRIES,
        TASK_RUN,
        {
          "force_update_tag": "test",
          "run_request": {
            "type": "DockerBuildRequest",
            "image_names": ["testtaskrun:v1"],
            "is_push_enabled": True,
            "no_cache": False,
            "docker_file_path": "Dockerfile",
            "platform": {
              "os": "linux",
              "architecture": "amd64"
            },
            "source_location": "https://github.com/Azure-Samples/acr-build-helloworld-node.git",
            "is_archive_enabled": True
          }
        }
    ).result()
    print("Update task run:\n{}".format(task_run))
    
    # Delete task run
    task_run = containerregistry_client.task_runs.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        TASK_RUN
    ).result()
    print("Delete task run.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

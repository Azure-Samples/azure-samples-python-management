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
    PIPELINE = "pipelinexxyyzz"
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

    # Create import pipeline
    pipeline = containerregistry_client.import_pipelines.begin_create(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
            # "user_assigned_identities": {}
          },
          "source": {
            "type": "AzureStorageBlobContainer",
            "uri": "https://accountname.blob.core.windows.net/containername",
            "key_vault_uri": "https://myvault.vault.azure.net/secrets/acrimportsas"
          },
          "options": [
            "OverwriteTags",
            "DeleteSourceBlobOnSuccess",
            "ContinueOnErrors"
          ]
        }
    ).result()
    print("Create import pipeline:\n{}".format(pipeline))

        # Create export pipeline
    pipeline = containerregistry_client.export_pipelines.begin_create(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
          },
          "target": {
            "type": "AzureStorageBlobContainer",
            "uri": "https://accountname.blob.core.windows.net/containername",
            "key_vault_uri": "https://myvault.vault.azure.net/secrets/acrexportsas"
          },
          "options": [
            "OverwriteBlobs"
          ]
        }
    ).result()
    print("Create import pipeline:\n{}".format(pipeline))

    # Get import pipeline
    pipeline = containerregistry_client.import_pipelines.get(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE
    )
    print("Get import pipeline:\n{}".format(pipeline))

    # Get export pipeline
    pipeline = containerregistry_client.export_pipelines.get(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE
    )
    print("Get export pipeline:\n{}".format(pipeline))

    # Delete import pipeline
    pipeline = containerregistry_client.import_pipelines.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE
    ).result()
    print("Delete import pipeline.\n")

    # Delete export pipeline
    pipeline = containerregistry_client.export_pipelines.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        PIPELINE
    ).result()
    print("Delete export pipeline.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

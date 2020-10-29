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
    WEBHOOK = "webhookxxyyzz"
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
    registries = containerregistry_client.registries.begin_create(
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
    # - end -

    # Create webhook
    webhook = containerregistry_client.webhooks.begin_create(
        GROUP_NAME,
        REGISTRIES,
        WEBHOOK,
        {
          "location": "eastus",
          "service_uri": "http://www.microsoft.com",
          "status": "enabled",
          "actions": [
            "push"
          ]
        }
    ).result()
    print("Create webhook:\n{}".format(webhook))

    # Get webhook
    webhook = containerregistry_client.webhooks.get(
        GROUP_NAME,
        REGISTRIES,
        WEBHOOK
    )
    print("Get webhook:\n{}".format(webhook))

    # Update webhook
    webhook = containerregistry_client.webhooks.begin_update(
        GROUP_NAME,
        REGISTRIES,
        WEBHOOK,
        {
          "location": "eastus",
          "service_uri": "http://www.microsoft.com",
          "status": "enabled",
          "actions": [
            "push"
          ]

        }
    ).result()
    print("Update webhook:\n{}".format(webhook))
    
    # Delete webhook
    webhook = containerregistry_client.webhooks.begin_delete(
        GROUP_NAME,
        REGISTRIES,
        WEBHOOK
    ).result()
    print("Delete webhook.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

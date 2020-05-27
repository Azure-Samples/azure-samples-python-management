# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.appconfiguration.aio import AppConfigurationManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    CONFIG_STORE_NAME = "configstorexyz"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    appconfig_client = AppConfigurationManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Init event loop
    event_loop = asyncio.get_event_loop()

    # Create resource group
    event_loop.run_until_complete(
        resource_client.resource_groups.create_or_update(
            GROUP_NAME,
            {"location": "eastus"}
        )
    )

    # Create appconfiguration store
    appconfig_store = event_loop.run_until_complete(
        appconfig_client.configuration_stores.create(
            GROUP_NAME,
            CONFIG_STORE_NAME,
            {
            "location": "eastus",
            "sku": {
                "name": "Standard"
            }
            }
        )
    )
    print("Create appconfigruation store:\n{}".format(appconfig_store))

    # Get appconfiguration store
    appconfig_store = event_loop.run_until_complete(
        appconfig_client.configuration_stores.get(
            GROUP_NAME,
            CONFIG_STORE_NAME
        )
    )
    print("Get appconfigruation store:\n{}".format(appconfig_store))

    # Update appconfiguration store
    appconfig_store = event_loop.run_until_complete(
        appconfig_client.configuration_stores.update(
            GROUP_NAME,
            CONFIG_STORE_NAME,
            {
            "tags": {
                "category": "Marketing"
            },
            "sku": {
                "name": "Standard"
            }
            }
        )
    )
    print("Update appconfigruation store:\n{}".format(appconfig_store))

    # Delete appconfiguration store
    event_loop.run_until_complete(
        appconfig_client.configuration_stores.delete(
            GROUP_NAME,
            CONFIG_STORE_NAME
        )
    )
    print("Delete appconfiguration store")

    # Delete Group
    event_loop.run_until_complete(
        resource_client.resource_groups.delete(
            GROUP_NAME
        )
    )

    # close event loop
    event_loop.run_until_complete(
        appconfig_client.close()
    )
    event_loop.run_until_complete(
        resource_client.close()
    )
    event_loop.close()

if __name__ == "__main__":
    main()

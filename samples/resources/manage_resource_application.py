# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredentials
from azure.mgmt.resource import ApplicationClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    GROUP_NAME_2 = "testgroupx2"
    APP_DEF_NAME = "applicationdefinition"
    APPLICATION_NAME = "applicationtest"

    # Create client
    app_client = ApplicationClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    resource_client.resource_groups.create_or_update(
        GROUP_NAME_2,
        {"location": "eastus"}
    )

    # Create application definition
    app_definition = app_client.application_definitions.begin_create_or_update(
        GROUP_NAME,
        APP_DEF_NAME,
        {
            "lock_level": "None",
            "display_name": "myManagedApplicationDef",
            "description": "myManagedApplicationDef description",
            "authorizations": [],
            "package_file_uri": "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-managed-application/artifacts/ManagedAppZip/pkg.zip",
            "location": "East US"
        }
    ).result()
    print("Create application definition: {}".format(app_definition))

    # Get application definition
    app_definition = app_client.application_definitions.get(
        GROUP_NAME,
        APP_DEF_NAME
    )
    print("Get application definition: {}".format(app_definition))

    # Create application
    app = app_client.applications.begin_create_or_update(
        GROUP_NAME,
        APPLICATION_NAME,
        {
            "application_definition_id": app_definition.id,
            "managed_resource_group_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/myManagedRG" + GROUP_NAME_2,
            "location": "East US",
            "kind": "ServiceCatalog"
        }
    )
    # ).result()
    print("Create application: {}".format(app))

    # Get application
    app = app_client.applications.get(
        GROUP_NAME,
        APPLICATION_NAME
    )
    print("Get application: {}".format(app))

    # Update application
    app = app_client.applications.update(
        GROUP_NAME,
        APPLICATION_NAME,
        {
            "managed_resource_group_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/myManagedRG" + GROUP_NAME_2,
            "kind": "ServiceCatalog"
        }
    )
    print("Update application: {}".format(app))

    # Delete application
    app_client.applications.begin_delete(
        GROUP_NAME,
        APPLICATION_NAME
    ).result()
    print("Delete application.")

    # Delete application definition
    app_client.application_definitions.begin_delete(
        GROUP_NAME,
        APP_DEF_NAME
    ).result()
    print("Delete appliation definition.")

if __name__ == "__main__":
    main()

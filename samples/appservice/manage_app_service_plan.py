# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    APP_SERVICE_PLAN = "appserviceplanxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    web_client = WebSiteManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create app service plan
    app_service_plan = web_client.app_service_plans.begin_create_or_update(
        GROUP_NAME,
        APP_SERVICE_PLAN,
        {
          "kind": "app",
          "location": "eastus",
          "sku": {
            "name": "P1",
            "tier": "Premium",
            "size": "P1",
            "family": "P",
            "capacity": "1"
          }
        }
    ).result()
    print("Create app service plan:\n{}".format(app_service_plan))

    # Get app service plan
    app_service_plan = web_client.app_service_plans.get(
        GROUP_NAME,
        APP_SERVICE_PLAN
    )
    print("Get app service plan:\n{}".format(app_service_plan))

    # Update app service plan
    app_service_plan = web_client.app_service_plans.update(
        GROUP_NAME,
        APP_SERVICE_PLAN,
        {
          "kind": "app"
        }
    )
    print("Update app service plan:\n{}".format(app_service_plan))
    
    # Delete app service plan
    app_service_plan = web_client.app_service_plans.delete(
        GROUP_NAME,
        APP_SERVICE_PLAN
    )
    print("Delete app service plan.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

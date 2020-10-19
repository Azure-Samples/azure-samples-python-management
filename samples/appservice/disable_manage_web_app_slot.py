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
    GROUP_NAME = "testgroupxx"
    WEB_APP_SLOT = "webappslotxxyyzzx"
    APP_SERVICE_PLAN = "appserviceplanx"
    WEB_APP = "webappxxxx"

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

    # - init depended resources -
    # Create app service plan
    plan = web_client.app_service_plans.begin_create_or_update(
        GROUP_NAME,
        APP_SERVICE_PLAN,
        {
          "location": "eastus",
          "sku": {
            "name": "B1",
            "tier": "BASIC",
            "capacity": "1"
          },
          "per_site_scaling": False,
          "is_xenon": False
        }
    ).result()

    # Create web app
    web_app = web_client.web_apps.begin_create_or_update(
        GROUP_NAME,
        WEB_APP,
        {
          "location": "eastus",
          "server_farm_id": plan.id,
          "reserved": False,
          "is_xenon": False,
          "hyper_v": False,
          "site_config": {
            "net_framework_version":"v4.6",
            "app_settings": [
              {"name": "WEBSITE_NODE_DEFAULT_VERSION", "value": "10.14"}
            ],
            "local_my_sql_enabled": False,
            "http20_enabled": True
          },
          "scm_site_also_stopped": False,
          "https_only": False
        }
    ).result()
    print("Create web app:\n{}".format(web_app))
    # - end -

    # Create web app slot
    web_app_slot = web_client.web_apps.begin_create_or_update_slot(
        GROUP_NAME,
        WEB_APP,
        WEB_APP_SLOT,
        {
          "location": "eastus",
          "reserved": False
          
        }
    ).result()
    print("Create web app slot:\n{}".format(web_app_slot))

    # Get web app slot
    web_app_slot = web_client.web_apps.get_slot(
        GROUP_NAME,
        WEB_APP,
        WEB_APP_SLOT
    )
    print("Get web app slot:\n{}".format(web_app_slot))

    # Update web app slot
    web_app_slot = web_client.web_apps.update_slot(
        GROUP_NAME,
        WEB_APP,
        WEB_APP_SLOT,
        {
          "location": "eastus",
          "properties": {
            "server_farm_id": plan.id,
            "reserved": False,
            "is_xenon": False,
            "hyper_v": False,
            "site_config": {
              "net_framework_version": "v4.6",
              "local_my_sql_enabled": False,
              "http20_enabled": True
            },
            "scm_site_also_stopped": False
          }
        }
    )
    print("Update web app slot:\n{}".format(web_app_slot))
    
    # Delete web app slot
    web_app_slot = web_client.web_apps.delete_slot(
        GROUP_NAME,
        WEB_APP_SLOT
    )
    print("Delete web app slot.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

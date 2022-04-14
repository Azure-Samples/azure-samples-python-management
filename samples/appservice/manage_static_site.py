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
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
    GROUP_NAME = "testgroupxx"
    STATIC_SITE = "staticsitexxyyzz"

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
        {"location": "eastus2"}
    )

    # Create static site
    static_site = web_client.static_sites.begin_create_or_update_static_site(
        GROUP_NAME,
        STATIC_SITE,
        {
          "location": "eastus2",
          "sku": {
            "name": "Free",
          },
          "repository_url": "https://github.com/00Kai0/html-docs-hello-world",
          "branch": "master",
          "repository_token": GITHUB_TOKEN,
          "build_properties": {
            "app_location": "app",
            "api_location": "api",
            "app_artifact_location": "build"
          }
        }
    )
    print("Create static site:\n{}".format(static_site))

    # Get static site
    static_site = web_client.static_sites.get_static_site(
        GROUP_NAME,
        STATIC_SITE
    )
    print("Get static site:\n{}".format(static_site))

    # Delete static site
    static_site = web_client.static_sites.begin_delete_static_site(
        GROUP_NAME,
        STATIC_SITE
    )
    print("Delete static site.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

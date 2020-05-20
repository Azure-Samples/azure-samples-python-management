# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ROUTE_FILTER = "route_filterxxyyzz"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create route filter
    route_filter = network_client.route_filters.begin_create_or_update(
        GROUP_NAME,
        ROUTE_FILTER,
        {
          "location": "eastus",
          "tags": {
            "key1": "value1"
          },
          "rules": []
        }
    ).result()
    print("Create route filter:\n{}".format(route_filter))

    # Get route filter
    route_filter = network_client.route_filters.get(
        GROUP_NAME,
        ROUTE_FILTER
    )
    print("Get route filter:\n{}".format(route_filter))

    # Update route filter
    route_filter = network_client.route_filters.update_tags(
        GROUP_NAME,
        ROUTE_FILTER,
        {
          "tags": {
            "key1": "value1"
          }
        }
    )
    print("Update route filter:\n{}".format(route_filter))
    
    # Delete route filter
    route_filter = network_client.route_filters.begin_delete(
        GROUP_NAME,
        ROUTE_FILTER
    ).result()
    print("Delete route filter.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

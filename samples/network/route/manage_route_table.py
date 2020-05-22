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
    ROUTE_TABLE = "route_tablexxyyzz"

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

    # Create route table
    route_table = network_client.route_tables.begin_create_or_update(
        GROUP_NAME,
        ROUTE_TABLE,
        {
          "location": "westus"
        }
    ).result()
    print("Create route table:\n{}".format(route_table))

    # Get route table
    route_table = network_client.route_tables.get(
        GROUP_NAME,
        ROUTE_TABLE
    )
    print("Get route table:\n{}".format(route_table))

    # Update route table
    route_table = network_client.route_tables.update_tags(
        GROUP_NAME,
        ROUTE_TABLE,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update route table:\n{}".format(route_table))
    
    # Delete route table
    route_table = network_client.route_tables.begin_delete(
        GROUP_NAME,
        ROUTE_TABLE
    ).result()
    print("Delete route table.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

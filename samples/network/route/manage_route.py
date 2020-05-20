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
    ROUTE = "routexxyyzz"
    ROUTE_TABLE = "route"

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

    # - init depended resources -
    # Create route table
    network_client.route_tables.begin_create_or_update(
        GROUP_NAME,
        ROUTE_TABLE,
        {
          "location": "westus"
        }
    ).result()
    # - end -

    # Create route
    route = network_client.routes.begin_create_or_update(
        GROUP_NAME,
        ROUTE_TABLE,
        ROUTE,
        {
          "address_prefix": "10.0.3.0/24",
          "next_hop_type": "VirtualNetworkGateway"
        }
    ).result()
    print("Create route:\n{}".format(route))

    # Get route
    route = network_client.routes.get(
        GROUP_NAME,
        ROUTE_TABLE,
        ROUTE
    )
    print("Get route:\n{}".format(route))

    # Delete route
    route = network_client.routes.begin_delete(
        GROUP_NAME,
        ROUTE_TABLE,
        ROUTE
    ).result()
    print("Delete route.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

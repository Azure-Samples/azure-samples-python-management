
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
    EXPRESS_ROUTE_CIRCUIT_AUTHORIZATION = "express_route_circuit_authorizationxxyyzz"
    EXPRESS_ROUTE_CIRCUIT = "expressroutecircuitxxzz"

    # Create client
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
    # Create express route circuit
    network_client.express_route_circuits.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        {
          "sku": {
            "name": "Standard_MeteredData",
            "tier": "Standard",
            "family": "MeteredData"
          },
          "location": "eastus",
          "service_provider_properties": {
            "service_provider_name": "Equinix",
            "peering_location": "Silicon Valley",
            "bandwidth_in_mbps": "200"
          }
        }
    ).result()
    # - end -

    # Create express route circuit authorization
    express_route_circuit_authorization = network_client.express_route_circuit_authorizations.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_AUTHORIZATION,
        {}
    ).result()
    print("Create express route circuit authorization:\n{}".format(express_route_circuit_authorization))

    # Get express route circuit authorization
    express_route_circuit_authorization = network_client.express_route_circuit_authorizations.get(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_AUTHORIZATION
    )
    print("Get express route circuit authorization:\n{}".format(express_route_circuit_authorization))

    # Delete express route circuit authorization
    express_route_circuit_authorization = network_client.express_route_circuit_authorizations.begin_delete(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_AUTHORIZATION
    ).result()
    print("Delete express route circuit authorization.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


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
    EXPRESS_ROUTE_CIRCUIT = "express_route_circuitxxyyzz"

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

    # Create express route circuit
    express_route_circuit = network_client.express_route_circuits.begin_create_or_update(
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
    print("Create express route circuit:\n{}".format(express_route_circuit))

    # Get express route circuit
    express_route_circuit = network_client.express_route_circuits.get(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT
    )
    print("Get express route circuit:\n{}".format(express_route_circuit))

    # Update express route circuit
    express_route_circuit = network_client.express_route_circuits.update_tags(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update express route circuit:\n{}".format(express_route_circuit))
    
    # Delete express route circuit
    express_route_circuit = network_client.express_route_circuits.begin_delete(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT
    ).result()
    print("Delete express route circuit.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

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
    EXPRESS_ROUTE_CIRCUIT_CONNECTION = "express_route_circuit_connectionxxyyzz"
    EXPRESS_ROUTE_CIRCUIT = "mycircuit1"
    EXPRESS_ROUTE_CIRCUIT_2 = "mycircuit2"
    EXPRESS_ROUTE_CIRCUIT_PEERING = "AzurePrivatePeering"  # The Express Route Bgp Peering Name must be equal to its PeeringType AzurePrivatePeering

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

    # Create express route circuit peering
    network_client.express_route_circuit_peerings.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_PEERING,
        {
          "peer_asn": "10001",
          "primary_peer_address_prefix": "102.0.0.0/30",
          "secondary_peer_address_prefix": "103.0.0.0/30",
          "vlan_id": "101"
        }
    ).result()

    # Create express route circuit
    network_client.express_route_circuits.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT_2,
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

    # Create express route circuit peering
    network_client.express_route_circuit_peerings.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT_2,
        EXPRESS_ROUTE_CIRCUIT_PEERING,
        {
          "peer_asn": "10002",
          "primary_peer_address_prefix": "104.0.0.0/30",
          "secondary_peer_address_prefix": "105.0.0.0/30",
          "vlan_id": "102"
        }
    ).result()
    # - end -

    # Create express route circuit connection
    express_route_circuit_connection = network_client.express_route_circuit_connections.begin_create_or_update(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_PEERING,
        EXPRESS_ROUTE_CIRCUIT_CONNECTION,
        {
            "express_route_circuit_peering": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/expressRouteCircuits/" + EXPRESS_ROUTE_CIRCUIT + "/peerings/" + EXPRESS_ROUTE_CIRCUIT_PEERING
            },
            "peer_express_route_circuit_peering": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/expressRouteCircuits/" + EXPRESS_ROUTE_CIRCUIT_2 + "/peerings/" + EXPRESS_ROUTE_CIRCUIT_PEERING 
            },
            "address_prefix": "104.0.0.0/29"
          }
    ).result()
    print("Create express route circuit connection:\n{}".format(express_route_circuit_connection))

    # Get express route circuit connection
    express_route_circuit_connection = network_client.express_route_circuit_connections.get(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_PEERING,
        EXPRESS_ROUTE_CIRCUIT_CONNECTION
    )
    print("Get express route circuit connection:\n{}".format(express_route_circuit_connection))

    # Delete express route circuit connection
    express_route_circuit_connection = network_client.express_route_circuit_connections.begin_delete(
        GROUP_NAME,
        EXPRESS_ROUTE_CIRCUIT,
        EXPRESS_ROUTE_CIRCUIT_PEERING,
        EXPRESS_ROUTE_CIRCUIT_CONNECTION
    ).result()
    print("Delete express route circuit connection.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

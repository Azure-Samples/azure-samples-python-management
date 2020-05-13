
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_NETWORK_GATEWAY_CONNECTION = "virtual_network_gateway_connectionxxyyzz"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # - end -

    # Create virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION,
        {
            # TODO: init resource body
        }
    ).result()
    print("Create virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))

    # Get virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.get(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION
    )
    print("Get virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))

    # Update virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION,
        {
            # TODO: init resource body
        }
    ).result()
    print("Update virtual network gateway connection:\n{}".format(virtual_network_gateway_connection))
    
    # Delete virtual network gateway connection
    virtual_network_gateway_connection = network_client.virtual_network_gateway_connections.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_GATEWAY_CONNECTION
    ).result()
    print("Delete virtual network gateway connection.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


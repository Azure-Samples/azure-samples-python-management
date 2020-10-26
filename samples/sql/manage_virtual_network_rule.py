# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    PASSWORD = os.environ.get("PASSWORD", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_NETWORK_RULE = "virtual_network_rulexxyyzz"
    SERVER = "serverxxy"
    NETWORK = "networkxxy"
    SUBNET = "subnetxxy"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    sql_client = SqlManagementClient(
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
    # Create Server
    server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        {
          "location": "eastus",
          "administrator_login": "dummylogin",
          "administrator_login_password": PASSWORD
        }
    ).result()
    print("Create server:\n{}".format(server))

    # Create virtual network
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    ).result()
    print("Create virtual network:\n{}".format(network))

    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK,
        SUBNET,
        {
            'address_prefix': '10.0.0.0/24',
        }
    ).result()
    print("Create subnet:\n{}".format(subnet))
    # - end -

    # Create virtual network rule
    virtual_network_rule = sql_client.virtual_network_rules.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        VIRTUAL_NETWORK_RULE,
        {
          "ignore_missing_vnet_service_endpoint": True,
          "virtual_network_subnet_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + NETWORK + "/subnets/" + SUBNET
        }
    ).result()
    print("Create virtual network rule:\n{}".format(virtual_network_rule))

    # Get virtual network rule
    virtual_network_rule = sql_client.virtual_network_rules.get(
        GROUP_NAME,
        SERVER,
        VIRTUAL_NETWORK_RULE
    )
    print("Get virtual network rule:\n{}".format(virtual_network_rule))

    # Delete virtual network rule
    virtual_network_rule = sql_client.virtual_network_rules.begin_delete(
        GROUP_NAME,
        SERVER,
        VIRTUAL_NETWORK_RULE
    ).result()
    print("Delete virtual network rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

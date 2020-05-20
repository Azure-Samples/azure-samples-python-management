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
    SECURITY_RULE = "security_rulexxyyzz"
    NETWORK_SECURITY_GROUP = "securitygroupxxx"

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
    # Create network security group
    network_client.network_security_groups.begin_create_or_update(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        {
          "location": "eastus"
        }
    ).result()
    # - end -

    # Create security rule
    security_rule = network_client.security_rules.begin_create_or_update(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        SECURITY_RULE,
        {
          "protocol": "*",
          "source_address_prefix": "10.0.0.0/8",
          "destination_address_prefix": "11.0.0.0/8",
          "access": "Deny",
          "destination_port_range": "8080",
          "source_port_range": "*",
          "priority": "100",
          "direction": "Outbound"
        }
    ).result()
    print("Create security rule:\n{}".format(security_rule))

    # Get security rule
    security_rule = network_client.security_rules.get(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        SECURITY_RULE
    )
    print("Get security rule:\n{}".format(security_rule))

    # Delete security rule
    security_rule = network_client.security_rules.begin_delete(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        SECURITY_RULE
    ).result()
    print("Delete security rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

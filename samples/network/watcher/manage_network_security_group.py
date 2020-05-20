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
    NETWORK_SECURITY_GROUP = "network_security_groupxxyyzz"

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

    # Create network security group
    network_security_group = network_client.network_security_groups.begin_create_or_update(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        {
          "location": "eastus"
        }
    ).result()
    print("Create network security group:\n{}".format(network_security_group))

    # Get network security group
    network_security_group = network_client.network_security_groups.get(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP
    )
    print("Get network security group:\n{}".format(network_security_group))

    # Update network security group
    network_security_group = network_client.network_security_groups.update_tags(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update network security group:\n{}".format(network_security_group))
    
    # Delete network security group
    network_security_group = network_client.network_security_groups.begin_delete(
        GROUP_NAME,
        NETWORK_SECURITY_GROUP
    ).result()
    print("Delete network security group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

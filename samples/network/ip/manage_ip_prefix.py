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
    PUBLIC_IP_PREFIX = "public_ip_prefixxxyyzz"

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

    # Create public ip prefix
    public_ip_prefix = network_client.public_ip_prefixes.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_PREFIX,
        {
          "location": "westus",
          "prefix_length": "30",
          "sku": {
            "name": "Standard"
          }
        }
    ).result()
    print("Create public ip prefix:\n{}".format(public_ip_prefix))

    # Get public ip prefix
    public_ip_prefix = network_client.public_ip_prefixes.get(
        GROUP_NAME,
        PUBLIC_IP_PREFIX
    )
    print("Get public ip prefix:\n{}".format(public_ip_prefix))

    # Update public ip prefix
    public_ip_prefix = network_client.public_ip_prefixes.update_tags(
        GROUP_NAME,
        PUBLIC_IP_PREFIX,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update public ip prefix:\n{}".format(public_ip_prefix))
    
    # Delete public ip prefix
    public_ip_prefix = network_client.public_ip_prefixes.begin_delete(
        GROUP_NAME,
        PUBLIC_IP_PREFIX
    ).result()
    print("Delete public ip prefix.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

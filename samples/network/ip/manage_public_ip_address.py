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
    PUBLIC_IP_ADDRESS = "public_ip_addressxxyyzz"

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

    # Create public ip address
    public_ip_address = network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS,
        {
          "location": "eastus"
        }
    ).result()
    print("Create public ip address:\n{}".format(public_ip_address))

    # Get public ip address
    public_ip_address = network_client.public_ip_addresses.get(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS
    )
    print("Get public ip address:\n{}".format(public_ip_address))

    # Update public ip address
    public_ip_address = network_client.public_ip_addresses.update_tags(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update public ip address:\n{}".format(public_ip_address))
    
    # Delete public ip address
    public_ip_address = network_client.public_ip_addresses.begin_delete(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS
    ).result()
    print("Delete public ip address.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


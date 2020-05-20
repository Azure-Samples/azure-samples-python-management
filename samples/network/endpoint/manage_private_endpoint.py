
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
    PRIVATE_ENDPOINT = "private_endpointxxyyzz"
    SERVICE_NAME = PRIVATE_LINK_SERVICE = "private_link_servicexxyyzz"
    LOAD_BALANCER_NAME = "loadbalancerxxx"
    IP_CONFIGURATION_NAME = "ipconfigurationxxx"
    VIRTUAL_NETWORK_NAME  = "virtualnetworkxxx"
    SUBNET = "subnetxxx"
    SUBNET_2 = "subnetxxxz"

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
    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "location": "eastus"
        }
    ).result()

    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET,
        {
          "address_prefix": "10.0.0.0/24",
          'private_link_service_network_policies': 'disabled'

        }
    ).result()

    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_2,
        {
          "address_prefix": "10.0.1.0/24",
          'private_endpoint_network_policies': 'disabled'

        }
    ).result()

    # Create load balancer
    network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LOAD_BALANCER_NAME,
        {
          "location": "eastus",
          "sku": {
            "name": "Standard"
          },
          "frontendIPConfigurations": [
            {
              "name": IP_CONFIGURATION_NAME,
              "subnet": {
                "id": subnet.id
              }
            }
          ]
        }
    ).result()

    # Create private link service
    network_client.private_link_services.begin_create_or_update(
        GROUP_NAME,
        PRIVATE_LINK_SERVICE,
        {
          "location": "eastus",
          "visibility": {
            "subscriptions": [
              SUBSCRIPTION_ID
            ]
          },
          "auto_approval": {
            "subscriptions": [
              SUBSCRIPTION_ID
            ]
          },
          "fqdns": [
            "fqdn1",
            "fqdn2",
            "fqdn3"
          ],
          "load_balancer_frontend_ip_configurations": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + IP_CONFIGURATION_NAME
            }
          ],
          "ip_configurations": [
            {
              "name": IP_CONFIGURATION_NAME,
              "private_ip_address": "10.0.1.4",
              "private_ipallocation_method": "Static",
              "private_ip_address_version": "IPv4",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET
              }
            }
          ]
        }
    ).result()
    # - end -

    # Create private endpoint
    private_endpoint = network_client.private_endpoints.begin_create_or_update(
        GROUP_NAME,
        PRIVATE_ENDPOINT,
        {
          "location": "eastus",
          "private_link_service_connections": [
            {
              "name": SERVICE_NAME,
              "private_link_service_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/privateLinkServices/" + SERVICE_NAME,
            }
          ],
          "subnet": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_2
          }
        }
    ).result()
    print("Create private endpoint:\n{}".format(private_endpoint))

    # Get private endpoint
    private_endpoint = network_client.private_endpoints.get(
        GROUP_NAME,
        PRIVATE_ENDPOINT
    )
    print("Get private endpoint:\n{}".format(private_endpoint))

    # Delete private endpoint
    private_endpoint = network_client.private_endpoints.begin_delete(
        GROUP_NAME,
        PRIVATE_ENDPOINT
    ).result()
    print("Delete private endpoint.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


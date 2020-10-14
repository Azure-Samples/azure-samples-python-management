# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE = "namespacexxyyzz"
    NETWORK_NAME = "mynetwork"
    SUBNET_NAME = "mysubnet"
    AUTHORIZATION_RULE_NAME = "myAuthorizationRule"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    servicebus_client = ServiceBusManagementClient(
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
    # Create Network
    azure_operation_poller = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        },
    )
    result_create = azure_operation_poller.result()

    async_subnet_creation = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )
    subnet_info = async_subnet_creation.result()
    # - end -

    # Create namespace
    namespace = servicebus_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
          "sku": {
            "name": "Premium",
            "tier": "Premium"
          },
          "location": "eastus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()
    print("Create namespace:\n{}".format(namespace))

    # Create namespace authorization rule
    rule = servicebus_client.namespaces.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        AUTHORIZATION_RULE_NAME,
        {
          "rights": [
            "Listen",
            "Send"
          ]
        }
    )
    print("Create name authorization rule:\n{}".format(rule))

    # Create namespace network rule set
    rule_set = servicebus_client.namespaces.create_or_update_network_rule_set(
        GROUP_NAME,
        NAMESPACE,
        {
          "default_action": "Deny",
          "virtual_network_rules": [
            {
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "ignore_missing_vnet_service_endpoint": True
            }
          ],
          "ip_rules": [
            {
              "ip_mask": "1.1.1.1",
              "action": "Allow"
            },
            {
              "ip_mask": "1.1.1.2",
              "action": "Allow"
            },
            {
              "ip_mask": "1.1.1.3",
              "action": "Allow"
            },
            {
              "ip_mask": "1.1.1.4",
              "action": "Allow"
            },
            {
              "ip_mask": "1.1.1.5",
              "action": "Allow"
            }
          ]
        }
    )
    print("Create network rule set:\n{}".format(rule_set))

    # Get namespace
    namespace = servicebus_client.namespaces.get(
        GROUP_NAME,
        NAMESPACE
    )
    print("Get namespace:\n{}".format(namespace))

    # Get authorization rule
    rule = servicebus_client.namespaces.get_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        AUTHORIZATION_RULE_NAME
    )
    print("Get authorization rule:\n{}".format(rule))

    # Get network rule set
    rule_set = servicebus_client.namespaces.get_network_rule_set(
        GROUP_NAME,
        NAMESPACE
    )
    print("Get network rule set:\n{}".format(rule_set))

    # Update namespace
    namespace = servicebus_client.namespaces.update(
        GROUP_NAME,
        NAMESPACE,
        {
          "location": "eastus",
          "tags": {
            "tag3": "value3",
            "tag4": "value4"
          }
        }
    )
    print("Update namespace:\n{}".format(namespace))
    
    # Delete namespace
    result = servicebus_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE
    )

    try:
        namespace = result.result()
    except HttpResponseError as e:
        if not str(e).startswith("(ResourceNotFound)"):
            raise e
    print("Delete namespace.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

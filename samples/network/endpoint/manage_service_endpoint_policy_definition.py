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
    SERVICE_ENDPOINT_POLICY = "serviceendpointpolicyxxx"
    SERVICE_ENDPOINT_POLICY_DEFINITION = "service_endpoint_policy_definitionxxyyzz"

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
    # Create service endpoint policy
    network_client.service_endpoint_policies.begin_create_or_update(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        {
          "location": "eastus"
        }
    ).result()
    # - end -

    # Create service endpoint policy definition
    service_endpoint_policy_definition = network_client.service_endpoint_policy_definitions.begin_create_or_update(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        SERVICE_ENDPOINT_POLICY_DEFINITION,
        {
          "description": "Storage Service EndpointPolicy Definition",
          "service": "Microsoft.Storage",
          "service_resources": [
            "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME
          ]
        }
    ).result()
    print("Create service endpoint policy definition:\n{}".format(service_endpoint_policy_definition))

    # Get service endpoint policy definition
    service_endpoint_policy_definition = network_client.service_endpoint_policy_definitions.get(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        SERVICE_ENDPOINT_POLICY_DEFINITION
    )
    print("Get service endpoint policy definition:\n{}".format(service_endpoint_policy_definition))
    
    # Delete service endpoint policy definition
    service_endpoint_policy_definition = network_client.service_endpoint_policy_definitions.begin_delete(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        SERVICE_ENDPOINT_POLICY_DEFINITION
    ).result()
    print("Delete service endpoint policy definition.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

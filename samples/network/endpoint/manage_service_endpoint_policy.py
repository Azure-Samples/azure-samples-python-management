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
    SERVICE_ENDPOINT_POLICY = "service_endpoint_policyxxyyzz"

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

    # Create service endpoint policy
    service_endpoint_policy = network_client.service_endpoint_policies.begin_create_or_update(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        {
          "location": "eastus"
        }
    ).result()
    print("Create service endpoint policy:\n{}".format(service_endpoint_policy))

    # Get service endpoint policy
    service_endpoint_policy = network_client.service_endpoint_policies.get(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY
    )
    print("Get service endpoint policy:\n{}".format(service_endpoint_policy))

    # Update service endpoint policy
    service_endpoint_policy = network_client.service_endpoint_policies.update_tags(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY,
        {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    )
    print("Update service endpoint policy:\n{}".format(service_endpoint_policy))
    
    # Delete service endpoint policy
    service_endpoint_policy = network_client.service_endpoint_policies.begin_delete(
        GROUP_NAME,
        SERVICE_ENDPOINT_POLICY
    ).result()
    print("Delete service endpoint policy.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

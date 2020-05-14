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
    FIREWALL_POLICY = "firewall_policyxxyyzz"

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

    # Create firewall policy
    firewall_policy = network_client.firewall_policies.begin_create_or_update(
        GROUP_NAME,
        FIREWALL_POLICY,
         {
          "tags": {
            "key1": "value1"
          },
          "location": "West US",
          "threat_intel_mode": "Alert"
        }
    ).result()
    print("Create firewall policy:\n{}".format(firewall_policy))

    # Get firewall policy
    firewall_policy = network_client.firewall_policies.get(
        GROUP_NAME,
        FIREWALL_POLICY
    )
    print("Get firewall policy:\n{}".format(firewall_policy))

    # Delete firewall policy
    firewall_policy = network_client.firewall_policies.begin_delete(
        GROUP_NAME,
        FIREWALL_POLICY
    ).result()
    print("Delete firewall policy.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

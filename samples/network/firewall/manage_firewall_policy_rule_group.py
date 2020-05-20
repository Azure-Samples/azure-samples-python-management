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
    FIREWALL_POLICY_RULE_GROUP = "firewall_policy_rule_groupxxyyzz"
    FIREWALL_POLICY = "firewall_policyxxx"

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
    # Create firewall policy
    network_client.firewall_policies.begin_create_or_update(
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
    # - end -

    # Create firewall policy rule group
    firewall_policy_rule_group = network_client.firewall_policy_rule_groups.begin_create_or_update(
        GROUP_NAME,
        FIREWALL_POLICY,
        FIREWALL_POLICY_RULE_GROUP,
        {
          "priority": "110",
          "rules": [
            {
              "rule_type": "FirewallPolicyFilterRule",
              "name": "Example-Filter-Rule",
              "action": {
                "type": "Deny"
              },
              "rule_conditions": [
                {
                  "rule_condition_type": "NetworkRuleCondition",
                  "name": "network-condition1",
                  "source_addresses": [
                    "10.1.25.0/24"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "ip_protocols": [
                    "TCP"
                  ],
                  "destination_ports": [
                    "*"
                  ]
                }
              ]
            }
          ]
        }
    ).result()
    print("Create firewall policy rule group:\n{}".format(firewall_policy_rule_group))

    # Get firewall policy rule group
    firewall_policy_rule_group = network_client.firewall_policy_rule_groups.get(
        GROUP_NAME,
        FIREWALL_POLICY,
        FIREWALL_POLICY_RULE_GROUP
    )
    print("Get firewall policy rule group:\n{}".format(firewall_policy_rule_group))

    # Delete firewall policy rule group
    firewall_policy_rule_group = network_client.firewall_policy_rule_groups.begin_delete(
        GROUP_NAME,
        FIREWALL_POLICY,
        FIREWALL_POLICY_RULE_GROUP
    ).result()
    print("Delete firewall policy rule group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

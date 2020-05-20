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
    WEB_APPLICATION_FIREWALL_POLICY = "web_application_firewall_policyxxyyzz"

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

    # Create web application firewall policy
    web_application_firewall_policy = network_client.web_application_firewall_policies.create_or_update(
        GROUP_NAME,
        WEB_APPLICATION_FIREWALL_POLICY,
        {
          "location": "WestUs",
          "managed_rules": {
            "managed_rule_sets": [
              {
                "rule_set_type": "OWASP",
                "rule_set_version": "3.0"
              }
            ]
          },
          "custom_rules": []
        }
    )
    print("Create web application firewall policy:\n{}".format(web_application_firewall_policy))

    # Get web application firewall policy
    web_application_firewall_policy = network_client.web_application_firewall_policies.get(
        GROUP_NAME,
        WEB_APPLICATION_FIREWALL_POLICY
    )
    print("Get web application firewall policy:\n{}".format(web_application_firewall_policy))

    # Delete web application firewall policy
    web_application_firewall_policy = network_client.web_application_firewall_policies.begin_delete(
        GROUP_NAME,
        WEB_APPLICATION_FIREWALL_POLICY
    ).result()
    print("Delete web application firewall policy.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

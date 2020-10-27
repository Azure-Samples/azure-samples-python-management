# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.policyinsights import PolicyInsightsClient
from azure.mgmt.resource import PolicyClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    REMEDIATION = "remediationxxyyzz"
    POLICY_NAME = "policyxyz"
    POLICY_ASSIGNMENT_NAME = "assignmentx"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    policyinsights_client = PolicyInsightsClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    policy_client = PolicyClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create policy definition
    definition = policy_client.policy_definitions.create_or_update(
        POLICY_NAME,
        {
            'policy_type': 'Custom',
            'description': 'Don\'t create a VM anywhere',
            'policy_rule': {
                'if': {
                  'allOf': [
                    {
                      'source': 'action',
                      'equals': 'Microsoft.Compute/virtualMachines/read'
                    },
                    {
                      'field': 'location',
                      'in': [
                        'eastus',
                        'eastus2',
                        'centralus'
                      ]
                    }
                  ]
                },
                'then': {
                  'effect': 'deny'
                }
            }
        }
    )
    print("Create policy definition: {}".format(definition))

    # Policy Assignment - By Name
    scope = '/subscriptions/{}/resourceGroups/{}'.format(
        SUBSCRIPTION_ID,
        GROUP_NAME
    )

    # Create policy assignment
    assignment = policy_client.policy_assignments.create(
        scope,
        POLICY_ASSIGNMENT_NAME,
        {
            'policy_definition_id': definition.id,
        }
    )
    print("Create policy assignment: {}".format(assignment))
    # - end -

    # Create remediation
    remediation = policyinsights_client.remediations.create_or_update_at_resource_group(
        GROUP_NAME,
        REMEDIATION,
        {
            "policy_assignment_id": assignment.id
        }
    )
    print("Create remediation:\n{}".format(remediation))

    # Get remediation
    remediation = policyinsights_client.remediations.get_at_resource_group(
        GROUP_NAME,
        REMEDIATION
    )
    print("Get remediation:\n{}".format(remediation))

    # Delete remediation
    remediation = policyinsights_client.remediations.delete_at_resource_group(
        GROUP_NAME,
        REMEDIATION
    )
    print("Delete remediation.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

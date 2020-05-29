# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import PolicyClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    POLICY_NAME = "policyxyz"
    POLICY_ASSIGNMENT_NAME = "assignmentx"
    POLICY_SET_NAME = "policysetdefinition"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    policy_client = PolicyClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

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

    # Get policy definition
    definition = policy_client.policy_definitions.get(
        POLICY_NAME
    )
    print("Get policy definition: {}".format(definition))

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

    # Get policy assignment
    assignment = policy_client.policy_assignments.get(
        assignment.scope,
        assignment.name
    )
    print("Get policy assignment: {}".format(assignment))

    # Create policy set definition
    policy_set = policy_client.policy_set_definitions.create_or_update(
        POLICY_SET_NAME,
        {
            "properties": {
                "displayName": "Cost Management",
                "description": "Policies to enforce low cost storage SKUs",
                "metadata": {
                    "category": "Cost Management"
                },
                "policyDefinitions": [
                    {
                        "policyDefinitionId": definition.id,
                        "parameters": {
                        }
                    }
                ]
            }
        }
    )
    print("Create policy set definition: {}".format(policy_set))

    # Get policy set definition
    policy_set = policy_client.policy_set_definitions.get(
        POLICY_SET_NAME
    )
    print("Get policy set definition: {}".format(policy_set))

    # Delete policy set definition
    policy_client.policy_set_definitions.delete(
        POLICY_SET_NAME
    )
    print("Delete policy set definition.")

    # Delete policy assignment
    policy_client.policy_assignments.delete(
        assignment.scope,
        assignment.name
    )
    print("Delete policy assignment.")

    # Delete policy definition
    policy_client.policy_definitions.delete(
        POLICY_NAME
    )
    print("Delete policy definition.")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

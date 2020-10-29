# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    CLIENT_OID = os.environ.get("CLIENT_OID", None)
    GROUP_NAME = "testgroupx"
    ROLE_ASSIGNMENT = "88888888-7000-0000-0000-000000000003"
    ROLE_DEFINITION = "e078ab98-ef3a-4c9a-aba7-12f5172b45d0"
    SCOPE = "subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}".format(
        subscriptionId=SUBSCRIPTION_ID,
        resourceGroupName=GROUP_NAME
    )       

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    authorization_client = AuthorizationManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        api_version="2018-01-01-preview"
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create role assignment
    role_assignment = authorization_client.role_assignments.create(
        SCOPE,
        ROLE_ASSIGNMENT,
        {
          "role_definition_id": "/subscriptions/" + SUBSCRIPTION_ID + "/providers/Microsoft.Authorization/roleDefinitions/" + ROLE_DEFINITION,
          "principal_id": CLIENT_OID,
        }
    )
    print("Create role assignment:\n{}".format(role_assignment))

    # Get role assignment
    role_assignment = authorization_client.role_assignments.get(
        SCOPE,
        ROLE_ASSIGNMENT
    )
    print("Get role assignment:\n{}".format(role_assignment))

    # Delete role assignment
    role_assignment = authorization_client.role_assignments.delete(
        SCOPE,
        ROLE_ASSIGNMENT
    )
    print("Delete role assignment.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

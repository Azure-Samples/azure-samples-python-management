# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.logic import LogicManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.logic.models import Workflow

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "logictest"
    WORKFLOW_NAME = '12HourHeartBeat'
    location="West US"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    logic_client = LogicManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": location}
    )

    # - init depended resources -
    # - end -

    # Create logic
    workflow = Workflow(
        location=location,
        definition={
            "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {},
            "triggers": {},
            "actions": {},
            "outputs": {}
        }
    )
    logic_client.workflows.create_or_update(
        GROUP_NAME,
        WORKFLOW_NAME,
        workflow
    )
    print("Create logic:\n")

    # Get logic
    logic_client.workflows.get(
        GROUP_NAME,
        WORKFLOW_NAME
    )
    print("Get logic:\n")
    
    # Delete logic
    logic_client.workflows.delete(
        GROUP_NAME,
        WORKFLOW_NAME
    )
    print("Delete logic.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

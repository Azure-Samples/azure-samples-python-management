# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.automation import AutomationClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RUNBOOK = "runbookxxyyzz"
    AUTOMATION_ACCOUNT = "automationaccountxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    automation_client = AutomationClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create automation account
    automation_account = automation_client.automation_account.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        {
          "sku": {
            "name": "Free"
          },
          "name": AUTOMATION_ACCOUNT,
          "location": "East US 2"
        }
    )
    print("Create automation account:\n{}".format(automation_account))
    # - end -

    # Create runbook
    runbook = automation_client.runbook.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK,
        {
          "log_verbose": False,
          "log_progress": False,
          "runbook_type": "PowerShellWorkflow",
          "draft": {},
          "description": "Description of the Runbook",
          "name": RUNBOOK,
          "location": "East US 2",
          "tags": {
            "tag01": "value01",
            "tag02": "value02",
          }
        }
    )
    print("Create runbook:\n{}".format(runbook))

    # Get runbook
    runbook = automation_client.runbook.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK
    )
    print("Get runbook:\n{}".format(runbook))

    # Update runbook
    runbook = automation_client.runbook.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK,
        {
          "description": "Updated Description of the Runbook",
          "log_verbose": False,
          "log_progress": True,
          "log_activity_trace": "1"
        }
    )
    print("Update runbook:\n{}".format(runbook))
    
    # Delete runbook
    runbook = automation_client.runbook.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK
    )
    print("Delete runbook.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

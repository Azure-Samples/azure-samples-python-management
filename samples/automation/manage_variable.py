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
    VARIABLE = "variablexxyyzz"
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

    # Create variable
    variable = automation_client.variable.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        VARIABLE,
        {
          "name": VARIABLE,
          "value": "\"ComputerName.domain.com\"",
          "description": "my description",
          "is_encrypted": False
        }
    )
    print("Create variable:\n{}".format(variable))

    # Get variable
    variable = automation_client.variable.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        VARIABLE
    )
    print("Get variable:\n{}".format(variable))

    # Update variable
    variable = automation_client.variable.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        VARIABLE,
        {
          "name": VARIABLE,
          "value": "\"ComputerName.domain.com\"",
          "description": "my description",
          "is_encrypted": False
        }
    )
    print("Update variable:\n{}".format(variable))
    
    # Delete variable
    variable = automation_client.variable.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        VARIABLE
    )
    print("Delete variable.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

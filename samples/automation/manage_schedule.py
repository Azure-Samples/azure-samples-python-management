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
    SCHEDULE = "schedulexxyyzz"
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

    # Create schedule
    schedule = automation_client.schedule.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE,
        {
          "name": SCHEDULE,
          "description": "my description of schedule goes here",
          "start_time": "2020-12-27T17:28:57.2494819Z",
          "expiry_time": "2021-01-01T17:28:57.2494819Z",
          "interval": "1",
          "frequency": "Hour"
        }
    )
    print("Create schedule:\n{}".format(schedule))

    # Get schedule
    schedule = automation_client.schedule.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE
    )
    print("Get schedule:\n{}".format(schedule))

    # Update schedule
    schedule = automation_client.schedule.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE,
        {
          "name": SCHEDULE,
          "description": "my updated description of schedule goes here",
          "is_enabled": False
        }
    )
    print("Update schedule:\n{}".format(schedule))
    
    # Delete schedule
    schedule = automation_client.schedule.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE
    )
    print("Delete schedule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

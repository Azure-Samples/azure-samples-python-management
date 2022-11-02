# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import uuid

from azure.identity import DefaultAzureCredential
from azure.mgmt.automation import AutomationClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RUNBOOK = "runbookxxyyzz"
    SCHEDULE = "schedulexxyyzz"
    JOB_SCHEDULE_ID = str(uuid.uuid4())
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
    print("\n Create automation account:\n{}".format(automation_account))
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
    print("\n Create runbook:\n{}".format(runbook))

    # Publish runbook
    automation_client.runbook.begin_publish(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK
    )
    print("\n Published runbook")
    
    # Get runbook
    runbook = automation_client.runbook.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK
    )
    print("\n Get runbook:\n{}".format(runbook))


    # Create schedule
    schedule = automation_client.schedule.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE,
        {
          "name": SCHEDULE,
          "description": "my description of schedule goes here",
          "start_time": "2022-10-31T08:15:00.2494819Z",
          "expiry_time": "2022-10-31T15:28:57.2494819Z",
          "interval": "1",
          "frequency": "Hour"
        }
    )
    print("\n Create schedule:\n{}".format(schedule))

    # Get schedule
    schedule = automation_client.schedule.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE
    )
    print("\n Get schedule:\n{}".format(schedule))

    # Create job schedule
    job_schedule = automation_client.job_schedule.create(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        JOB_SCHEDULE_ID,
        {
            "schedule": {
              "name": SCHEDULE
            },
            "runbook": {
              "name": RUNBOOK
            },
            "parameters": {
              "jobscheduletag01": "jobschedulevalue01",
              "jobscheduletag02": "jobschedulevalue02"
            }
        }
    )
    print("\n Create job schedule:\n{}".format(job_schedule))
 
    # Get job schedule
    job_schedule = automation_client.job_schedule.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        JOB_SCHEDULE_ID
    )
    print("\n Get job schedule:\n{}".format(job_schedule))
    
    # Delete job schedule
    job_schedule = automation_client.job_schedule.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        JOB_SCHEDULE_ID
    )
    print("\n Delete job schedule.\n")    
    
    # Delete schedule
    schedule = automation_client.schedule.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        SCHEDULE
    )
    print("\n Delete schedule.\n")
    
    # Delete runbook
    runbook = automation_client.runbook.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK
    )
    print("\n Delete runbook.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

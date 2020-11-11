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
    WEBHOOK = "webhookxxyyzz"
    AUTOMATION_ACCOUNT = "automationaccountxxyyzz"
    RUNBOOK = "Get-AzureVMTutorial"

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

    # Create runbook
    runbook = automation_client.runbook.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        RUNBOOK,
        {
          "log_verbose": False,
          "log_progress": True,
          "runbook_type": "PowerShellWorkflow",
          "publish_content_link": {
            "uri": "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/0.0.0.3/101-automation-runbook-getvms/Runbooks/Get-AzureVMTutorial.ps1",
            "content_hash": {
              "algorithm": "SHA256",
              "value": "4fab357cab33adbe9af72ae4b1203e601e30e44de271616e376c08218fd10d1c"
            },
          },
          "description": "Description of the Runbook",
          "log_activity_trace": "1",
          "name": RUNBOOK,
          "location": "East US 2",
          "tags": {
            "tag01": "value01",
            "tag02": "value02"
          }
        }
    )
    print("Create runbook:\n{}".format(runbook))
    # - end -

    # Create webhook
    webhook = automation_client.webhook.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        WEBHOOK,
        {
          "name": "TestWebhook",
          "is_enabled": True,
          "uri": "https://s1events.azure-automation.net/webhooks?token=7u3KfQvM1vUPWaDMFRv2%2fAA4Jqx8QwS8aBuyO6Xsdcw%3d",
          "expiry_time": "2021-03-29T22:18:13.7002872Z",
          "runbook": {
            "name": RUNBOOK
          }
        }
    )
    print("Create webhook:\n{}".format(webhook))

    # Get webhook
    webhook = automation_client.webhook.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        WEBHOOK
    )
    print("Get webhook:\n{}".format(webhook))

    # Update webhook
    webhook = automation_client.webhook.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        WEBHOOK,
        {
          "name": WEBHOOK,
          "is_enabled": False,
          "description": "updated webhook"
        }
    )
    print("Update webhook:\n{}".format(webhook))
    
    # Delete webhook
    webhook = automation_client.webhook.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        WEBHOOK
    )
    print("Delete webhook.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

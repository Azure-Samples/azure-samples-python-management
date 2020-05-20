# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredentials
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    WORKSPACE_NAME = "workspacex"
    SCHEDULED_QUERY_RULE = "scheduledqueryrule"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    loganalytics_client = LogAnalyticsManagementClient(
        credentials=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )


    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create workspace
    workspace = loganalytics_client.workspaces.create_or_update(
        GROUP_NAME,
        WORKSPACE_NAME,
        {
          "sku": {
            "name": "PerNode"
          },
          "retention_in_days": 30,
          "location": "eastus",
          "tags": {
            "tag1": "val1"
          }
        }
    ).result()

    # Create scheduled query rule
    schedueld_query_rule = monitor_client.scheduled_query_rules.create_or_update(
        GROUP_NAME,
        SCHEDULED_QUERY_RULE,
        {
          "location": "eastus",
          "description": "log alert description",
          "enabled": "true",
          "provisioning_state": "Succeeded",
          "source": {
            "query": "Heartbeat | summarize AggregatedValue = count() by bin(TimeGenerated, 5m)",
            "data_source_id": workspace.id,
            "query_type": "ResultCount"
          },
          "schedule": {
            "frequency_in_minutes": "15",
            "time_window_in_minutes": "15"
          },
          "action": {
            "odata.type": "Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction",
            "severity": "1",
            "azns_action": {
              "action_group": [],
              "email_subject": "Email Header",
              "custom_webhook_payload": "{}"
            },
            "trigger": {
              "threshold_operator": "GreaterThan",
              "threshold": "3",
              "metric_trigger": {
                "threshold_operator": "GreaterThan",
                "threshold": "5",
                "metric_trigger_type": "Consecutive",
                "metric_column": "Computer"
              }
            }
          }
        }
    )
    print("Create scheduled query rule:\n{}".format(schedueld_query_rule))

    # Get scheduled query rule
    schedueld_query_rule = monitor_client.scheduled_query_rules.get(
        GROUP_NAME,
        SCHEDULED_QUERY_RULE
    )
    print("Get scheduled query rule:\n{}".format(schedueld_query_rule))

    # Patch scheduled query rule
    schedueld_query_rule = monitor_client.scheduled_query_rules.update(
        GROUP_NAME,
        SCHEDULED_QUERY_RULE,
        {
          "enabled": "true"
        }
    )
    print("Update scheduled query rule:\n{}".format(schedueld_query_rule))

    # Delete scheduled query rule
    monitor_client.scheduled_query_rules.delete(
        GROUP_NAME,
        SCHEDULED_QUERY_RULE
    )
    print("Delete scheduled query rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

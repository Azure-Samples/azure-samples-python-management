# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import EnvironmentCredential
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.loganalytics import OperationalInsightsManagementClient
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.logic import LogicManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


# Cerdential for track1 sdk
credential4track1 = ServicePrincipalCredentials(
    client_id=os.environ.get("AZURE_CLIENT_ID"),
    secret=os.environ.get("AZURE_CLIENT_SECRET"),
    tenant=os.environ.get("AZURE_TENANT_ID")
)

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT_NAME = "storagex"
    NAMESPACE = "namespacex"
    EVENTHUB = "eventhub"
    AUTHORIZATION_RULE = "authorizationx"
    INSIGHT = "insightx"
    WORKSPACE_NAME = "workspacex"
    WORKFLOW_NAME = "workflow"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    eventhub_client = EventHubManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # use track1 sdk
    loganalytics_client = OperationalInsightsManagementClient(
        credentials=credential4track1,
        subscription_id=SUBSCRIPTION_ID
    )
    logic_client = LogicManagementClient(
        credentials=credential4track1,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Storage
    storage_account = storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            "sku":{
                "name": "Standard_LRS"
            },
            "kind": "Storage",
            "location": "eastus",
            "enable_https_traffic_only": True
        }
    ).result()

    # Create eventhub authorization rule
    eventhub_client.namesapces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "eastus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    eventhub_client.namespaces.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        AUTHORIZATION_RULE,
        {
          "rights": [
            "Listen",
            "Send",
            "Manage"
          ]
        }
    )

    eventhub_client.event_hubs.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        EVENTHUB,
        {
          "message_retention_in_days": "4",
          "partition_count": "4",
          "status": "Active",
          "capture_description": {
            "enabled": True,
            "encoding": "Avro",
            "interval_in_seconds": "120",
            "size_limit_in_bytes": "10485763",
            "destination": {
              "name": "EventHubArchive.AzureBlockBlob",
              "storage_account_resource_id": storage_account.id,
              "blob_container": "container",
              "archive_name_format": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
            }
          }
        }
    )

    eventhub_client.event_hubs.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        EVENTHUB,
        AUTHORIZATION_RULE,
        {
          "rights": [
            "Listen",
            "Send",
            "Manage"
          ]
        }
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

    # Create workflow
    workflow = logic_client.workflows.create_or_update(
        GROUP_NAME,
        WORKFLOW_NAME,
        {
            "location": "eastus",
            "definition":{
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {},
                "triggers": {},
                "actions": {},
                "outputs": {}
            }
        }
    )
    RESOURCE_URI = workflow.id

    # Create diagnostic setting
    diagnostic_setting = monitor_client.create_or_update(
        RESOURCE_URI,
        INSIGHT,
        {
          "storage_account_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME + "",
          "workspace_id": workspace.id,
          "event_hub_authorization_rule_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/microsoft.eventhub/namespaces/" + NAMESPACE + "/authorizationrules/" + AUTHORIZATION_RULE,
          "event_hub_name": EVENTHUB,
          "metrics": [],
          "logs": [
            {
              "category": "WorkflowRuntime",
              "enabled": True,
              "retention_policy": {
                "enabled": False,
                "days": "0"
              }
            }
          ],
        }
    )
    print("Create diagnostic setting:\n{}".format(diagnostic_setting))

    # Get diagnostic setting
    diagnostic_setting = monitor_client.get(
        RESOURCE_URI,
        INSIGHT
    )
    print("Get diagnostic setting:\n{}".format(diagnostic_setting))

    # Delete diagnostic setting
    monitor_client.delete(
        RESOURCE_URI,
        INSIGHT
    )
    print("Delete diagnostic setting.")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

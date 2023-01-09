import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient


def main():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credentials = DefaultAzureCredential()
    GROUP_NAME = "test"
    workspace_name = "testWorkspace"
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    log_analytics_client = LogAnalyticsManagementClient(credentials, subscription_id, )
    #
    loganalytics_client = LogAnalyticsManagementClient(credentials, subscription_id, )
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}

    )

    log_analytics_client.workspaces.begin_create_or_update(
        resource_group_name='zb_test',
        workspace_name='oiautorest6685',
        parameters={
            "location": "australiasoutheast",
            "properties": {"retentionInDays": 30, "sku": {"name": "PerGB2018"}},
            "tags": {"tag1": "val1"},
        },
    ).result()

    response = log_analytics_client.tables.list_by_workspace(
        resource_group_name='zb_test',
        workspace_name='oiautorest6685'
    )
    for item in response:
        print(item)

    loganalytics_client.workspaces.begin_delete(
        GROUP_NAME,
        workspace_name
    ).result()

    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == '__main__':
    main()

import os
from msrestazure.azure_cloud import AZURE_US_GOV_CLOUD
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient


def main():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credentials = DefaultAzureCredential()
    GROUP_NAME = "test"
    workspace_name="testWorkspace"
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    #
    loganalytics_client_gov = LogAnalyticsManagementClient(credentials, subscription_id,
                                                           base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager,
                                                           credential_scopes=[
                                                               AZURE_US_GOV_CLOUD.endpoints.resource_manager + ".default"])
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    loganalytics = loganalytics_client_gov.workspaces.begin_create_or_update(
        GROUP_NAME,
        workspace_name,
        {"location": "eastus"}
    )
    print("Create consumption:\n{}\n".format(loganalytics))

    loganalytics = loganalytics_client_gov.workspaces.list()
    print("List consumption:\n{}\n".format(loganalytics))

    loganalytics = loganalytics_client_gov.workspaces.get(
        GROUP_NAME,
        workspace_name
    )
    print("Get consumption:\n{}\n".format(loganalytics))

    loganalytics = loganalytics_client_gov.workspaces.begin_delete(
        GROUP_NAME,
        workspace_name
    )
    print("Delete consumption:\n{}\n".format(loganalytics))


if __name__ == "__main__":
    main()

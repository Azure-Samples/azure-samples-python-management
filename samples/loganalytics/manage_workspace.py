import os
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
    loganalytics_client_gov = LogAnalyticsManagementClient(credentials, subscription_id,)
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}

    )

    loganalytics=loganalytics_client_gov.workspaces.begin_create_or_update(
        GROUP_NAME,
        workspace_name,
        {"location": "eastus"}
    ).result()
    print("Create consumption:\n{}\n".format(loganalytics))

    loganalytics=loganalytics_client_gov.workspaces.list()
    print("List consumption:")
    for loganalytics_list in loganalytics:
        print(loganalytics_list)

    loganalytics=loganalytics_client_gov.workspaces.get(
        GROUP_NAME,
        workspace_name
    )
    print("\nGet consumption:\n{}\n".format(loganalytics))


    loganalytics=loganalytics_client_gov.workspaces.begin_delete(
        GROUP_NAME,
        workspace_name
    )
    print("Delete consumption:\n{}\n".format(loganalytics))




if __name__ == "__main__":
    main()

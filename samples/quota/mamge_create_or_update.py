import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.quota import AzureQuotaExtensionAPI
from azure.mgmt.resource import ResourceManagementClient


def main():
    subscription = os.getenv('AZURE_SUBSCRIPTION_ID')
    quota_client = AzureQuotaExtensionAPI(DefaultAzureCredential(), subscription)
    resource_client = ResourceManagementClient(DefaultAzureCredential(), subscription)

    GROUP_NAME = 'zbw_test'

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    result = quota_client.quota.begin_create_or_update(
        resource_name=GROUP_NAME,
        scope='/subscriptions/' + subscription + 'providers/Microsoft.Compute/location/easrus',
        create_quota_request={
            "properties": {
                "limit": 200,
                "name": {
                    "value": GROUP_NAME
                }
            }
        }
    ).result()
    print(result)

    # delete resource group
    resource_client.resource_groups.begin_delete(GROUP_NAME).result()


if __name__ == '__main__':
    main()

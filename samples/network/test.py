import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from dotenv import load_dotenv

# This sample is just to show how to customize response if needed
def main():

    load_dotenv()
    credentials = DefaultAzureCredential()
    subscription = os.getenv('AZURE_SUBSCRIPTION_ID')

    def callback(response):
        # print raw response content
        print(response.http_response.internal_response.content)

    compute_client = ComputeManagementClient(credentials, subscription)
    print("compute raw response content contains format info:")
    list(compute_client.usage.list(location="eastus", raw_response_hook=callback))

    network_client = NetworkManagementClient(credentials, subscription)
    print("network raw response content contains format info:")
    list(network_client.usages.list(location="eastus", raw_response_hook=callback))

    storage_client = StorageManagementClient(credentials, subscription)
    print("storage raw response content contains no format info:")
    list(storage_client.usages.list_by_location(location="eastus", raw_response_hook=callback))

if __name__ == '__main__':
    main()

import json
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient


# This sample is just to show how to customize response if needed
def main():

    credentials = DefaultAzureCredential()
    subscription = os.getenv('SUBSCRIPTION_ID')

    def callback(response):
        origin_req = json.loads(response.http_response.internal_response.text)
        with open('result.json', 'w') as file:
            file.write(json.dumps(origin_req, indent=4))

    nmclient = NetworkManagementClient(credentials, subscription)

    virtual_network_gateway = nmclient.network_managers.get(
        resource_group_name='resource_group_name',
        network_manager_name='network_manager_name',
        raw_response_hook=callback
    )


if __name__ == '__main__':
    main()

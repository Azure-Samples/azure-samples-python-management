import json
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetworkGateway


# This sample is just to show how to customize request if needed
def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('SUBSCRIPTION_ID')

    def callback(request):
        origin_req = json.loads(request.http_request.body)
        with open('result.json', 'w') as file:
            file.write(json.dumps(origin_req, indent=4))

    client = NetworkManagementClient(credentials, subscription)

    virtual_network_gateway = client.virtual_network_gateways.begin_create_or_update(
        resource_group_name='GROUP_NAME',
        vm_name='NEW_VIRTUAL_NETWORK_GATEWAY',
        parameters='vn_para',
        raw_request_hook=callback
    ).result()


if __name__ == '__main__':
    main()

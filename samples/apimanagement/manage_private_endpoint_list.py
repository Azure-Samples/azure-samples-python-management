import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.apimanagement import ApiManagementClient
from azure.mgmt.apimanagement.models import ApiManagementServiceResource, ApiManagementServiceSkuProperties

GROUP_NAME = 'testgroupx'
LOCATION = 'eastus2'
SERVICE_NAME = 'test-apimanager'
PUBLISHER_NAME = 'foo'
PUBLISHER_EMAIL = 'foo@foo.com'

def main():

    SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')

    resource_client = ResourceManagementClient(
        DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    apimanagement_client = ApiManagementClient(
        DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    resource_group = resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})

    # create and update may take a long time
    apimanagement_parameters = ApiManagementServiceResource(
        sku=ApiManagementServiceSkuProperties(name="Developer", capacity=1),
        location=LOCATION,
        publisher_name=PUBLISHER_NAME,
        publisher_email=PUBLISHER_EMAIL,
        enable_client_certificate=True
    )

    apimanagement_service = apimanagement_client.api_management_service.begin_create_or_update(GROUP_NAME, SERVICE_NAME,
                                                                                               parameters=apimanagement_parameters).result()

    result = apimanagement_client.private_endpoint_connection.list_private_link_resources(GROUP_NAME, SERVICE_NAME)

    for i in result.value:
        print(i)

    apimanagement_client.api_management_service.begin_delete(GROUP_NAME, SERVICE_NAME)
    resource_client.resource_groups.begin_delete(GROUP_NAME)

    print('Finish')

if __name__ == '__main__':
    main()
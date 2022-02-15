# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.communication import CommunicationServiceManagementClient
from azure.mgmt.communication.models import CommunicationServiceResource

def main():

    credential = DefaultAzureCredential()
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxx"
    COMMUNICATION_NAME = 'test-communicationxxx'

    # Create client
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    communication_client = CommunicationServiceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_group = resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )
    print("Create a resource group:\n{}".format(resource_group))

    # Create Communication
    communication = communication_client.communication_service.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        communication_service_name=COMMUNICATION_NAME,
        parameters=CommunicationServiceResource(location="global", data_location="United States")
    ).result()
    print('Create a communication service:\n{}'.format(communication))

    # Get Communication
    communication_res = communication_client.communication_service.get(
        resource_group_name=GROUP_NAME,
        communication_service_name=COMMUNICATION_NAME
    )
    print('Get a communication service:\n{}'.format(communication_res))

    # Delete Communication
    communication_client.communication_service.begin_delete(
        resource_group_name=GROUP_NAME,
        communication_service_name=COMMUNICATION_NAME
    ).result()
    print('Delete a communication service.')

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()
    print('Delete a resource group.')


if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.iothub import IotHubClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    IOT_HUB_RESOURCE = "iothubresourcexxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    iothub_client = IotHubClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create iot hub resource
    iot_hub_resource = iothub_client.iot_hub_resource.begin_create_or_update(
        GROUP_NAME,
        IOT_HUB_RESOURCE,
        {
            'location': "eastus",
            'subscriptionid': SUBSCRIPTION_ID,
            'resourcegroup': GROUP_NAME,
            'sku': {
                'name': 'S1',
                'capacity': 2
            },
            'properties': {
                'enable_file_upload_notifications': False,
                'operations_monitoring_properties': {
                'events': {
                    "C2DCommands": "Error",
                    "DeviceTelemetry": "Error",
                    "DeviceIdentityOperations": "Error",
                    "Connections": "Information"
                }
                },
                "features": "None",
            }
        }
    ).result()
    print("Create iot hub resource:\n{}".format(iot_hub_resource))

    # Get iot hub resource
    iot_hub_resource = iothub_client.iot_hub_resource.get(
        GROUP_NAME,
        IOT_HUB_RESOURCE
    )
    print("Get iot hub resource:\n{}".format(iot_hub_resource))

    # Delete iot hub resource
    iot_hub_resource = iothub_client.iot_hub_resource.begin_delete(
        GROUP_NAME,
        IOT_HUB_RESOURCE
    ).result()
    print("Delete iot hub resource.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

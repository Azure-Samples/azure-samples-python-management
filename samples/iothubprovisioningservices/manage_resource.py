# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.iothubprovisioningservices import IotDpsClient, models
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    IOT_DPS_RESOURCE = "iotdpsresourcexxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    iotdps_client = IotDpsClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Get iot dps resource
    iot_dps_resource = iotdps_client.iot_dps_resource.begin_create_or_update(
        GROUP_NAME,
        IOT_DPS_RESOURCE,
        {
          "location": "eastus",
          "subscriptionid": SUBSCRIPTION_ID,
          "resourcegroup": GROUP_NAME,
          "type": "Microsoft.Devices/ProvisioningServices",
          "sku": {
            "name": "S1",
            "tier": "Standard",
            "capacity": "1"
          },
          "properties": {}
        }
    ).result()
    print("Create iot dps resource:\n{}".format(iot_dps_resource))

    # Get iot dps resource
    iot_dps_resource = iotdps_client.iot_dps_resource.get(
        IOT_DPS_RESOURCE,
        GROUP_NAME
    )
    print("Get iot hub resource:\n{}".format(iot_dps_resource))

    # Delete iot dps resource
    iot_dps_resource = iotdps_client.iot_dps_resource.begin_delete(
        IOT_DPS_RESOURCE,
        GROUP_NAME
    ).result()
    print("Delete iot dps resource.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

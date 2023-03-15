# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resourceconnector import Appliances
from azure.mgmt.resourceconnector.models import Appliance

# If you want to see the log, please deannotate the following code:
# import sys
# import logging
#
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     stream=sys.stdout)

def main():
    sub_id = os.environ.get("SUBSCRIPTION_ID", None)
    group_name = "testgroupx"
    resource_name = "resourceconnector"
    location = "eastus"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )
    client = Appliances(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        group_name,
        {"location": location},
    )

    # - init depended resources -
    # Create virtual network
    result = client.appliances.begin_create_or_update(
        group_name,
        resource_name,
        Appliance(location=location),
        headers={"x-ms-client-request-id": "4159a480-c203-11ed-b9e5-6045bdc724a6"},
        params={"api-version": "2021-10-31-preview"}
    ).result()
    print("result of begin_create_or_update: {}".format(result.serialize()))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        group_name
    ).result()


if __name__ == "__main__":
    main()

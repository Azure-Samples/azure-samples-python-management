# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.devtestlabs import DevTestLabsClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.','')
    GROUP_NAME = "testdevtestlabs" + TIME
    DEVTESTLABS = "devtestlabs" + TIME
    LOCATION = 'eastus'

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    devtestlabs_client = DevTestLabsClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": LOCATION}
    )

    # - init depended resources -
    # - end -

    # Create devtestlabs
    devtestlabs = devtestlabs_client.labs.begin_create_or_update(
        GROUP_NAME,
        DEVTESTLABS,
        {'location': LOCATION}
    ).result()
    print("Create devtestlabs:\n{}".format(devtestlabs))

    # Get devtestlabs
    devtestlabs = devtestlabs_client.labs.get(
        GROUP_NAME,
        DEVTESTLABS
    )
    print("Get devtestlabs:\n{}".format(devtestlabs))

    # Update devtestlabs
    BODY = {
        "properties": {
            "labStorageType": "Premium"
        }
    }
    devtestlabs = devtestlabs_client.labs.update(
        GROUP_NAME,
        DEVTESTLABS,
        BODY
    )
    print("Update devtestlabs:\n{}".format(devtestlabs))
    
    # Delete devtestlabs
    devtestlabs = devtestlabs_client.labs.begin_delete(
        GROUP_NAME,
        DEVTESTLABS
    ).result()
    print("Delete devtestlabs.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

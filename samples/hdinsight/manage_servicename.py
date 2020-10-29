# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.hdinsight import HDInsightManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


# - other dependence -
# - end -


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.', '')
    GROUP_NAME = "testhdinsight" + TIME
    STORAGE = "storage" + TIME
    HDINSIGHT = "hdinsight" + TIME

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    hdinsight_client = HDInsightManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create storage
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE,
        {
            "location": "eastus",
            "sku": {'name': 'Standard_LRS'},
            "kind": 'StorageV2',
            'enable_https_traffic_only': True,
        }
    ).result()

    # - init depended resources -
    # - end -

    # Create hdinsight
    hdinsight = hdinsight_client.hdinsights.begin_create(
        GROUP_NAME,
        HDINSIGHT,
        {
            # TODO: init resource body
        }
    ).result()
    print("Create hdinsight:\n{}\n".format(hdinsight))

    # Get hdinsight
    hdinsight = hdinsight_client.hdinsights.get(
        GROUP_NAME,
        HDINSIGHT
    )
    print("Get hdinsight:\n{}\n".format(hdinsight))

    # Update hdinsight
    hdinsight = hdinsight_client.hdinsights.begin_update(
        GROUP_NAME,
        HDINSIGHT,
        {
            # TODO: init resource body
        }
    ).result()
    print("Update hdinsight:\n{}\n".format(hdinsight))

    # Delete hdinsight
    hdinsight = hdinsight_client.hdinsights.begin_delete(
        GROUP_NAME,
        HDINSIGHT
    ).result()
    print("Delete hdinsight.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

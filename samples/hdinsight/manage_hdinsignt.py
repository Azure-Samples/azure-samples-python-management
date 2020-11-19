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


# - other dependence -
# - end -


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.', '')
    GROUP_NAME = "testhdinsight" + TIME

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
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

    # - init depended resources -
    # - end -

    # Create hdinsight
    hdinsight_client.operations.list()
    print("operations:\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout)

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RESOURCE_NAME = "pytestresource"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Check resource existence
    result = resource_client.resources.check_existence(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.Web",
        parent_resource_path="",
        resource_type="sites",
        resource_name=RESOURCE_NAME,
        api_version="2021-04-01"
    )
    print(result)


if __name__ == "__main__":
    main()

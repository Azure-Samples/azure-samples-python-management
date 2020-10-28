# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.search import SearchManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    QUERY_KEY = "query_keyxxyyzz"
    SERVICE = "servicexxyz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    search_client = SearchManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create service
    service = search_client.services.begin_create_or_update(
        GROUP_NAME,
        SERVICE,
        {
            'location': "eastus",
            'replica_count': 1,
            'partition_count': 1,
            'hosting_mode': 'Default',
            'sku': {
                'name': 'standard'
            }
        }
    ).result()
    print("Create service:\n{}".format(service))
    # - end -

    # Create query key
    query_key = search_client.query_keys.create(
        GROUP_NAME,
        SERVICE,
        QUERY_KEY
    )
    print("Create query key:\n{}".format(query_key))

    # List query key
    query_keys = search_client.query_keys.list_by_search_service(
        GROUP_NAME,
        SERVICE
    )
    print("List query key:\n{}".format(list(query_keys)))

    # Delete query key
    query_key = search_client.query_keys.delete(
        GROUP_NAME,
        SERVICE,
        QUERY_KEY
    )
    print("Delete query key.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

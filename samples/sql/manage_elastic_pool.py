# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ELASTIC_POOL = "elastic_poolxxyyzz"
    SERVER = "serverxxyz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    sql_client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create Server
    server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        {
          "location": "eastus",
          "administrator_login": "dummylogin",
          "administrator_login_password": "Un53cuRE!"
        }
    ).result()
    print("Create server:\n{}".format(server))
    # - end -

    # Create elastic pool
    elastic_pool = sql_client.elastic_pools.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        ELASTIC_POOL,
        {
          "location": "eastus"
        }
    ).result()
    print("Create elastic pool:\n{}".format(elastic_pool))

    # Get elastic pool
    elastic_pool = sql_client.elastic_pools.get(
        GROUP_NAME,
        SERVER,
        ELASTIC_POOL
    )
    print("Get elastic pool:\n{}".format(elastic_pool))

    # Update elastic pool
    elastic_pool = sql_client.elastic_pools.begin_update(
        GROUP_NAME,
        SERVER,
        ELASTIC_POOL,
        {}
    ).result()
    print("Update elastic pool:\n{}".format(elastic_pool))
    
    # Delete elastic pool
    elastic_pool = sql_client.elastic_pools.begin_delete(
        GROUP_NAME,
        SERVER,
        ELASTIC_POOL
    ).result()
    print("Delete elastic pool.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

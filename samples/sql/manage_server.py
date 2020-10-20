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
    SERVER = "serverxxyyzz"

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

    # Create server
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

    # Get server
    server = sql_client.servers.get(
        GROUP_NAME,
        SERVER
    )
    print("Get server:\n{}".format(server))

    # Update server
    server = sql_client.servers.begin_update(
        GROUP_NAME,
        SERVER,
        {
          "administrator_login": "dummylogin",
          "administrator_login_password": "Un53cuRE!"
        }
    ).result()
    print("Update server:\n{}".format(server))
    
    # Delete server
    server = sql_client.servers.begin_delete(
        GROUP_NAME,
        SERVER
    ).result()
    print("Delete server.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

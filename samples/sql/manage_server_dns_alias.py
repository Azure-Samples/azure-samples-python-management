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
    SERVER_DNS_ALIAS = "serverdnsaliasxxyyzz"
    SERVER = "serverxxy"

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

    # Create server dns alias
    server_dns_alias = sql_client.server_dns_aliases.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        SERVER_DNS_ALIAS
    ).result()
    print("Create server dns alias:\n{}".format(server_dns_alias))

    # Get server dns alias
    server_dns_alias = sql_client.server_dns_aliases.get(
        GROUP_NAME,
        SERVER,
        SERVER_DNS_ALIAS
    )
    print("Get server dns alias:\n{}".format(server_dns_alias))

    # Delete server dns alias
    server_dns_alias = sql_client.server_dns_aliases.begin_delete(
        GROUP_NAME,
        SERVER,
        SERVER_DNS_ALIAS
    ).result()
    print("Delete server dns alias.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

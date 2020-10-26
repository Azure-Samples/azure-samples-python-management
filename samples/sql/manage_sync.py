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
    PASSWORD = os.environ.get("PASSWORD", None)
    GROUP_NAME = "testgroupx"
    SERVER = "serverxxy"
    DATABASE = "databasexxy"
    SYNC_DATABASE = "syncdatabasexxy"
    SYNC_GROUP = "syncgroupxxy"
    SYNC_MEMBER = "syncmemberxxy"
    SYNC_AGENT = "syncagentxxxy"

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
          "administrator_login_password": PASSWORD
        }
    ).result()
    print("Create server:\n{}".format(server))

    # Create Database
    database = sql_client.databases.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        {
          "location": "eastus"
        }
    ).result()
    print("Create database:\n{}".format(database))

    sync_database = sql_client.databases.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        SYNC_DATABASE,
        {
          "location": "eastus"
        }
    ).result()
    print("Create sync database:\n{}".format(sync_database))
    # - end -

    # Create sync agent
    sync_agent = sql_client.sync_agents.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        SYNC_AGENT,
        {
          "sync_database_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Sql/servers/" + SERVER + "/databases/" + SYNC_DATABASE
        }
    ).result()
    print("Create sync agent:\n{}".format(sync_agent))

    # Create sync group
    sync_group = sql_client.sync_groups.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        SYNC_GROUP,
        {
          "interval": "-1",
          "conflict_resolution_policy": "HubWin",
          "sync_database_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Sql/servers/" + SERVER + "/databases/" + SYNC_DATABASE,
          "hub_database_user_name": "hubUser",
          "use_private_link_connection": False
        }
    ).result()
    print("Create sync group:\n{}".format(sync_group))

    # Create sync member
    sync_member = sql_client.sync_members.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        SYNC_GROUP,
        SYNC_MEMBER,
        {
          "database_type": "AzureSqlDatabase",
          "server_name": SERVER,
          "database_name": DATABASE, 
          "user_name": "dummylogin",
          "password": PASSWORD,
          "sync_direction": "Bidirectional",
          "use_private_link_connection": False,
          "sync_state": "UnProvisioned"
        }
    ).result()
    print("Create sync member:\n{}".format(sync_member))

    # Get sync member
    sync_member = sql_client.sync_members.get(
        GROUP_NAME,
        SERVER,
        DATABASE,
        SYNC_GROUP,
        SYNC_MEMBER
    )
    print("Get sync member:\n{}".format(sync_member))

    # Update sync member
    sync_member = sql_client.sync_members.begin_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        SYNC_GROUP,
        SYNC_MEMBER,
        {
          "use_private_link_connection": False
        }
    ).result()
    print("Update sync member:\n{}".format(sync_member))
    
    # Delete sync member
    sql_client.sync_members.begin_delete(
        GROUP_NAME,
        SERVER,
        DATABASE,
        SYNC_GROUP,
        SYNC_MEMBER
    ).result()
    print("Delete sync member.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

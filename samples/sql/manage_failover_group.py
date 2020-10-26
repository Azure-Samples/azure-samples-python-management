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
    FAILOVER_GROUP = "failovergroupxxyyzz"
    SERVER = "serverxxyz"
    PARTNER_SERVER = "partnerserverxxyz"

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

    partner_server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        PARTNER_SERVER,
        {
          "location": "eastus2",
          "administrator_login": "dummylogin",
          "administrator_login_password": PASSWORD
        }
    ).result()
    print("Create server:\n{}".format(partner_server))
    # - end -

    # Create failover group
    failover_group = sql_client.failover_groups.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        FAILOVER_GROUP,
        {
          "read_write_endpoint": {
            "failover_policy": "Automatic",
            "failover_with_data_loss_grace_period_minutes": "480"
          },
          "read_only_endpoint": {
            "failover_policy": "Disabled"
          },
          "partner_servers": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Sql/servers/" + PARTNER_SERVER
            }
          ],
          "databases": [
          ]
        }
    ).result()
    print("Create failover group:\n{}".format(failover_group))

    # Get failover group
    failover_group = sql_client.failover_groups.get(
        GROUP_NAME,
        SERVER,
        FAILOVER_GROUP
    )
    print("Get failover group:\n{}".format(failover_group))

    # Update failover group
    failover_group = sql_client.failover_groups.begin_update(
        GROUP_NAME,
        SERVER,
        FAILOVER_GROUP,
        {
          "read_write_endpoint": {
            "failover_policy": "Automatic",
            "failover_with_data_loss_grace_period_minutes": "120"
          },
          "databases": [
          ]
        }
    ).result()
    print("Update failover group:\n{}".format(failover_group))
    
    # Delete failover group
    failover_group = sql_client.failover_groups.begin_delete(
        GROUP_NAME,
        SERVER,
        FAILOVER_GROUP
    ).result()
    print("Delete failover group.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

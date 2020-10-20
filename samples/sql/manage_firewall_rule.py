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
    FIREWALL_RULE = "firewall_rulexxyyzz"
    SERVER = "serverxx"

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

    # Create firewall rule
    firewall_rule = sql_client.firewall_rules.create_or_update(
        GROUP_NAME,
        SERVER,
        FIREWALL_RULE,
        {
          "start_ip_address": "0.0.0.3",
          "end_ip_address": "0.0.0.3"
        }
    )
    print("Create firewall rule:\n{}".format(firewall_rule))

    # Get firewall rule
    firewall_rule = sql_client.firewall_rules.get(
        GROUP_NAME,
        SERVER,
        FIREWALL_RULE
    )
    print("Get firewall rule:\n{}".format(firewall_rule))

    # Delete firewall rule
    firewall_rule = sql_client.firewall_rules.delete(
        GROUP_NAME,
        SERVER,
        FIREWALL_RULE
    )
    print("Delete firewall rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

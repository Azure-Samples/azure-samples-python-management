# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxx"
    DATABASE_ACCOUNT = "myaccountxx"
    TABLE_NAME = "myTable"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    cosmosdb_client = CosmosDBManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create database account
    database_account = cosmosdb_client.database_accounts.begin_create_or_update(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        {
          "location": "eastus",
          "kind": "GlobalDocumentDB",
          "database_account_offer_type": "Standard",
          "locations": [
            {
              "location_name": "eastus",
              "is_zone_redundant": False,
              "failover_priority": "0"
            }
          ],
          "capabilities": [{
            "name": "EnableTable"
          }],
          "api_properties": {}
        }
    ).result()
    print("Create database account:\n{}".format(database_account))
    # - end -

    # Create table
    table = cosmosdb_client.table_resources.begin_create_update_table(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        TABLE_NAME,
        {
          "location": "eastus",
          "resource": {
            "id": TABLE_NAME
          },
          "options": {}
        }
    ).result()
    print("Create table:\n{}".format(table))

    # Delete table
    cosmosdb_client.table_resources.begin_delete_table(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        TABLE_NAME
    ).result()
    print("Delete table.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

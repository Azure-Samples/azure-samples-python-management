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
    GROUP_NAME = "testgroupx"
    DATABASE_ACCOUNT = "databaseaccountxxyyzz"

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

    # Create database account
    database_account = cosmosdb_client.database_accounts.begin_create_or_update(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        {
          "location": "eastus",
          "database_account_offer_type": "Standard",
          "locations": [
            {
              "failover_priority": "2",
              "location_name": "southcentralus",
              "is_zone_redundant": False
            },
            {
              "location_name": "eastus",
              "failover_priority": "1"
            },
            {
              "location_name": "westus",
              "failover_priority": "0"
            }
          ]
        }
    ).result()
    print("Create database account:\n{}".format(database_account))

    # Get database account
    database_account = cosmosdb_client.database_accounts.get(
        GROUP_NAME,
        DATABASE_ACCOUNT
    )
    print("Get database account:\n{}".format(database_account))

    # Update database account
    database_account = cosmosdb_client.database_accounts.begin_update(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        {
          "tags": {
            "dept": "finance"
          }
        }
    ).result()
    print("Update database account:\n{}".format(database_account))
    
    # Delete database account
    database_account = cosmosdb_client.database_accounts.begin_delete(
        GROUP_NAME,
        DATABASE_ACCOUNT
    ).result()
    print("Delete database account.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

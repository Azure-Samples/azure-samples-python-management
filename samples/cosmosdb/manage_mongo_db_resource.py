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
    DATABASE_ACCOUNT = "databaseaccountxxyyzzk"
    DATABASE_NAME = "myDatabase"
    COLLECTION_NAME = "myCollection"

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
          "kind": "MongoDB",
          "database_account_offer_type": "Standard",
          "locations": [
            {
              "location_name": "eastus",
              "is_zone_redundant": False,
              "failover_priority": "0"
            }
          ],
          "api_properties": {}
        }
    ).result()
    print("Create database account:\n{}".format(database_account))
    # - end -

    # Create mongodb database
    database = cosmosdb_client.mongo_db_resources.begin_create_update_mongo_db_database(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME,
        {
          "location": "eastus",
          "resource": {
            "id": DATABASE_NAME
          },
          "options": {
            "throughput": "2000"
          }
        }
    ).result()
    print("Create mongodb database:\n{}".format(database))

    # Create mongodb collection
    collection = cosmosdb_client.mongo_db_resources.begin_create_update_mongo_db_collection(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME,
        COLLECTION_NAME,
        {
          "location": "eastus",
          "resource": {
            "id": COLLECTION_NAME,
            "shard_key": {
              "theShardKey": "Hash"
            }
          },
          "options": {
            "throughput": "2000"
          }
        }
    )
    print("Create mongodb collection:\n{}".format(collection))

    # Get mongodb database
    database = cosmosdb_client.mongo_db_resources.get_mongo_db_database(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME
    )
    print("Get mongodb database:\n{}".format(database))

    # Delete mongodb database 
    cosmosdb_client.mongo_db_resources.begin_delete_mongo_db_database(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME
    ).result()
    print("Delete mongodb database.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

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
    DATABASE_ACCOUNT = "mydatabaseaccount"
    DATABASE_NAME = "myDatabase"
    CONTAINER_NAME = "myContainer"

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
          "api_properties": {}
        }
    ).result()
    print("Create database account:\n{}".format(database_account))
    # - end -

    # Create sql database
    database = cosmosdb_client.sql_resources.begin_create_update_sql_database(
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
    print("Create sql database:\n{}".format(database))

    # Create sql container
    container = cosmosdb_client.sql_resources.begin_create_update_sql_container(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME,
        CONTAINER_NAME,
        {
          "location": "eastus",
          "resource": {
            "id": CONTAINER_NAME,
            "indexing_policy": {
              "indexing_mode": "Consistent",
              "automatic": True,
              "included_paths": [
                {
                  "path": "/*",
                  "indexes": [
                    {
                      "kind": "Range",
                      "data_type": "String",
                      "precision": "-1"
                    },
                    {
                      "kind": "Range",
                      "data_type": "Number",
                      "precision": "-1"
                    }
                  ]
                }
              ],
              "excluded_paths": []
            },
            "partition_key": {
              "paths": [
                "/AccountNumber"
              ],
              "kind": "Hash"
            },
            "default_ttl": "100",
            "unique_key_policy": {
              "unique_keys": [
                {
                  "paths": [
                    "/testPath"
                  ]
                }
              ]
            },
            "conflict_resolution_policy": {
              "mode": "LastWriterWins",
              "conflict_resolution_path": "/path"
            }
          },
          "options": {
            "throughput": "2000"
          }
        }
    ).result()
    print("Create sql container:\n{}".format(container))

    # Get sql database
    database = cosmosdb_client.sql_resources.get_sql_database(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME
    )
    print("Get sql database:\n{}".format(database))

    # Delete sql database
    cosmosdb_client.sql_resources.begin_delete_sql_database(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME
    ).result()
    print("Delete sql database.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

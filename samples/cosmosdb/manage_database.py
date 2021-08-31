# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.cosmos import CosmosClient


def _format(content):
    return json.dumps(content.serialize(keep_readonly=True), indent=4, separators=(',', ': '))


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxxx"
    DATABASE_ACCOUNT = "databaseaccount20210831"
    DATABASE_NAME = 'database000'

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
    print("Create database account:\n{}".format(_format(database_account)))

    # Get database account
    database_account = cosmosdb_client.database_accounts.get(
        GROUP_NAME,
        DATABASE_ACCOUNT
    )

    print("Get database account:\n{}".format(_format(database_account)))

    # List database account keys
    database_account_keys = cosmosdb_client.database_accounts.list_keys(
        GROUP_NAME,
        DATABASE_ACCOUNT
    )
    print("List database account keys:\n{}".format(_format(database_account_keys)))

    # Create database under database account
    url = database_account.document_endpoint
    key = database_account_keys.primary_master_key
    cosmos_client = CosmosClient(url, credential=key)
    cosmos_client.create_database(DATABASE_NAME)

    # List database metrics
    database = cosmosdb_client.database.list_metrics(
        GROUP_NAME,
        DATABASE_ACCOUNT,
        DATABASE_NAME,
        "(name.value eq 'Available Storage' or name.value eq 'Data Size' or name.value eq 'Index Size') and timeGrain eq duration'PT5M'"
    )
    for item in database:
        print("Get database:\n{}".format(_format(item)))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

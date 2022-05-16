import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.storage import StorageManagementClient

def main():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credentials = DefaultAzureCredential()
    GROUP_NAME = "test"
    export_name="exportxxyyzz"
    scope=f'subscriptions/{subscription_id}/resourceGroups/{GROUP_NAME}'
    STORAGE_ACCOUNT = "storageaccountxxyyzz"

    resource_client = ResourceManagementClient(
        credentials,
        subscription_id
    )
    storage_client = StorageManagementClient(
        credentials,
        subscription_id
    )
    costmanagement_client = CostManagementClient(
        credentials
    )
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}

    )
    storage_account = storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": "eastus",
            "encryption": {
                "services": {
                    "file": {
                        "key_type": "Account",
                        "enabled": True
                    },
                    "blob": {
                        "key_type": "Account",
                        "enabled": True
                    }
                },
                "key_source": "Microsoft.Storage"
            },
            "tags": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    ).result()
    costmanagement=costmanagement_client.exports.create_or_update(
        scope,
        export_name,
        {
            'id':storage_account.id,
            'name':STORAGE_ACCOUNT,
            'type':'Daily',
            "format": "Csv",
            "delivery_info": {
                "destination":{
                    "resourceId":storage_account.id,
                    "container": "exports",
                    "rootFolderPath": "ad-hoc"
                }
            },
            "definition": {
                "type": "Usage",
                "timeframe": "MonthToDate",
            },
            "schedule": {
                "status": "Active",
                "recurrence": "Weekly",
                "recurrencePeriod": {
                    "from": "2022-05-13T12:00:00Z",
                    "to": "2022-10-31T00:00:00Z"
                }
            }

        }

    )
    print("Create consumption:\n{}\n".format(costmanagement))

    costmanagement_client.exports.delete(
        scope,
        export_name
    )
    print("Delete exports.\n")


    storage_client.storage_accounts.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT
    )
    print("Delete storage.\n")

    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()



if __name__ == "__main__":
    main()

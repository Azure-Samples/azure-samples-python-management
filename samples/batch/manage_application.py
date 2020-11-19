# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import io
import os

import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.batch import BatchManagement
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT = "storageaccountxxyzz"
    ACCOUNT = "accountxx"
    APPLICATION = "applicationxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    batch_client = BatchManagement(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create storage account
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
    print("Create storage account:\n{}".format(storage_account))
    
    # Create account
    account = batch_client.batch_account.begin_create(
        GROUP_NAME,
        ACCOUNT,
        {
            "location": "eastus",
            "auto_storage": {
                "storage_account_id": storage_account.id
            }
        }
    ).result()
    print("Create batch account:\n{}".format(account))
    # - end -

    # Create application
    application = batch_client.application.create(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION,
        {
            "display_name": "my_application_name",
            "allow_updates": True
        }
    )
    print("Create application:\n{}".format(application))

    # Create application package
    package = batch_client.application_package.create(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION,
        "v1.0"
    )
    print("Create package:\n{}".format(package))

    # Get application
    application = batch_client.application.get(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION
    )
    print("Get application:\n{}".format(application))

    with io.BytesIO(b'Hello World') as f:
        headers = {'x-ms-blob-type': 'BlockBlob'}
        upload = requests.put(package.storage_url, headers=headers, data=f.read())
        if not upload:
            raise ValueError('Upload failed: {!r}'.format(upload))

    # Activate package
    batch_client.application_package.activate(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION,
        "v1.0",
        {
            "format": "zip"
        }
    )
    print("Activate application.\n")

    # Update application
    application = batch_client.application.update(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION,
        {
            "allow_updates": False,
            "display_name": "my_updated_name",
            "default_version": "v1.0"
        }
    )
    print("Update application:\n{}".format(application))

    # Delete package
    batch_client.application_package.delete(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION,
        "v1.0"
    )
    print("Delete package.\n")
    
    # Delete application
    application = batch_client.application.delete(
        GROUP_NAME,
        ACCOUNT,
        APPLICATION
    )
    print("Delete application.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

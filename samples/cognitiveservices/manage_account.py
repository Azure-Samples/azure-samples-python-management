# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ACCOUNT = "accountxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    cognitiveservices_client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create account
    account = cognitiveservices_client.accounts.create(
        GROUP_NAME,
        ACCOUNT,
        {
          "location": "West US",
          "kind": "CognitiveServices",
          "sku": {
            "name": "S0"
          },
          "identity": {
            "type": "SystemAssigned"
          }
        }
    )
    print("Create account:\n{}".format(account))

    # Get account
    account = cognitiveservices_client.accounts.get_properties(
        GROUP_NAME,
        ACCOUNT
    )
    print("Get account:\n{}".format(account))

    # Update account
    account = cognitiveservices_client.accounts.update(
        GROUP_NAME,
        ACCOUNT,
        {
          "location": "West US",
          "kind": "CognitiveServices",
          "sku": {
            "name": "S0"
          },
          "identity": {
            "type": "SystemAssigned"
          }
        }
    )
    print("Update account:\n{}".format(account))
    
    # Delete account
    account = cognitiveservices_client.accounts.delete(
        GROUP_NAME,
        ACCOUNT
    )
    print("Delete account.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

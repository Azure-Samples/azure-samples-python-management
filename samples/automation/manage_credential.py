# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.automation import AutomationClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    CREDENTIAL = "credentialxxyyzz"
    AUTOMATION_ACCOUNT = "automationaccountxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    automation_client = AutomationClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create automation account
    automation_account = automation_client.automation_account.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        {
          "sku": {
            "name": "Free"
          },
          "name": AUTOMATION_ACCOUNT,
          "location": "East US 2"
        }
    )
    print("Create automation account:\n{}".format(automation_account))
    # - end -

    # Create credential
    credential = automation_client.credential.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        CREDENTIAL,
        {
          "name": CREDENTIAL,
          "user_name": "mylingaiah",
          "password": "myPassw0rd",
          "description": "my description goes here"
        }
    )
    print("Create credential:\n{}".format(credential))

    # Get credential
    credential = automation_client.credential.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        CREDENTIAL
    )
    print("Get credential:\n{}".format(credential))

    # Update credential
    credential = automation_client.credential.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        CREDENTIAL,
        {
          "name": CREDENTIAL,
          "user_name": "mylingaiah",
          "password": "myPassw0rd",
          "description": "my description goes here"
        }
    )
    print("Update credential:\n{}".format(credential))
    
    # Delete credential
    credential = automation_client.credential.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        CREDENTIAL
    )
    print("Delete credential.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

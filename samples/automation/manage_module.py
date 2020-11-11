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
    MODULE = "modulexxyyzz"
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

    # Create module
    module = automation_client.module.create_or_update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        MODULE,
        {
          "content_link": {
            "uri": "https://teststorage.blob.core.windows.net/dsccomposite/OmsCompositeResources.zip",
            "content_hash": {
              "algorithm": "sha265",
              "value": "07E108A962B81DD9C9BAA89BB47C0F6EE52B29E83758B07795E408D258B2B87A"
            },
            "version": "1.0.0.0"
          }
        }
    )
    print("Create module:\n{}".format(module))

    # Get module
    module = automation_client.module.get(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        MODULE
    )
    print("Get module:\n{}".format(module))

    # Update module
    module = automation_client.module.update(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        MODULE,
        {
          "content_link": {
            "uri": "https://teststorage.blob.core.windows.net/dsccomposite/OmsCompositeResources.zip",
            "content_hash": {
              "algorithm": "sha265",
              "value": "07E108A962B81DD9C9BAA89BB47C0F6EE52B29E83758B07795E408D258B2B87A"
            },
            "version": "1.0.0.0"
          }
        }
    )
    print("Update module:\n{}".format(module))
    
    # Delete module
    module = automation_client.module.delete(
        GROUP_NAME,
        AUTOMATION_ACCOUNT,
        MODULE
    )
    print("Delete module.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

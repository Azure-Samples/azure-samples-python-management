# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VAULT = "vaultxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    recoveryservices_client = RecoveryServicesClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create vault
    vault = recoveryservices_client.vaults.create_or_update(
        GROUP_NAME,
        VAULT,
        {
            "location": "eastus",
            "sku": {
                "name": "standard"
            },
            "properties": {}
        }
    )
    print("Create vault:\n{}".format(vault))

    # Get vault
    vault = recoveryservices_client.vaults.get(
        GROUP_NAME,
        VAULT
    )
    print("Get vault:\n{}".format(vault))

    # Update vault
    vault = recoveryservices_client.vaults.update(
        GROUP_NAME,
        VAULT,
        {
            "location": "eastus",
            "sku": {
                "name": "standard"
            },
            "properties": {}
        }
    )
    print("Update vault:\n{}".format(vault))
    
    # Delete vault
    vault = recoveryservices_client.vaults.delete(
        GROUP_NAME,
        VAULT
    )
    print("Delete vault.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    TENANT_ID = os.environ.get("AZURE_TENANT_ID", None)
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VAULT = "vaultxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    keyvault_client = KeyVaultManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create vault
    vault = keyvault_client.vaults.begin_create_or_update(
        GROUP_NAME,
        VAULT,
        {
          "location": "eastus",
          "properties": {
            "tenant_id": TENANT_ID,
            "sku": {
              "family": "A",
              "name": "standard"
            },
            "access_policies": [
              {
                "tenant_id": TENANT_ID,
                "object_id": "00000000-0000-0000-0000-000000000000",
                "permissions": {
                  "keys": [
                    "encrypt",
                    "decrypt",
                    "wrapKey",
                    "unwrapKey",
                    "sign",
                    "verify",
                    "get",
                    "list",
                    "create",
                    "update",
                    "import",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge"
                  ],
                  "secrets": [
                    "get",
                    "list",
                    "set",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge"
                  ],
                  "certificates": [
                    "get",
                    "list",
                    "delete",
                    "create",
                    "import",
                    "update",
                    "managecontacts",
                    "getissuers",
                    "listissuers",
                    "setissuers",
                    "deleteissuers",
                    "manageissuers",
                    "recover",
                    "purge"
                  ]
                }
              }
            ],
            "enabled_for_deployment": True,
            "enabled_for_disk_encryption": True,
            "enabled_for_template_deployment": True
          }
        }
    ).result()
    print("Create vault:\n{}".format(vault))

    # Get vault
    vault = keyvault_client.vaults.get(
        GROUP_NAME,
        VAULT
    )
    print("Get vault:\n{}".format(vault))

    # Update vault
    vault = keyvault_client.vaults.update(
        GROUP_NAME,
        VAULT,
        {
            "tags": {
                "category": "Marketing"
            }
        }
    )
    print("Update vault:\n{}".format(vault))
    
    # Delete vault
    keyvault_client.vaults.delete(
        GROUP_NAME,
        VAULT
    )
    print("Delete vault.\n")

    # Purge a deleted vault
    keyvault_client.vaults.begin_purge_deleted(
        VAULT,
        "eastus"
    ).result()
    print("Purge a deleted vault.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

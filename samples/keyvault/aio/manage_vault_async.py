# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.keyvault.aio import KeyVaultManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    TENANT_ID = os.environ.get("AZURE_TENANT_ID", None)
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VAULT = "vaultxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    keyvault_client = KeyVaultManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create vault
    async_poller = await keyvault_client.vaults.begin_create_or_update(
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
    )
    vault = await async_poller.result()
    print("Create vault:\n{}".format(vault))

    # Get vault
    vault = await keyvault_client.vaults.get(
        GROUP_NAME,
        VAULT
    )
    print("Get vault:\n{}".format(vault))

    # List vault (List operation will return asyncList)
    vaults = list()
    async for v in keyvault_client.vaults.list_by_resource_group(GROUP_NAME, top="1"):
        vaults.append(v)
    print("List vaults:\n{}".format(vaults))

    # Update vault
    vault = await keyvault_client.vaults.update(
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
    await keyvault_client.vaults.delete(
        GROUP_NAME,
        VAULT
    )
    print("Delete vault.\n")

    # Purge a deleted vault
    async_poller = await keyvault_client.vaults.begin_purge_deleted(
        VAULT,
        "eastus"
    )
    await async_poller.result()
    print("Purge a deleted vault.\n")

    # Delete Group
    async_poller = await resource_client.resource_groups.begin_delete(
        GROUP_NAME
    )
    await async_poller.result()

    # [Warning] All clients and credentials need to be closed.
    # link: https://github.com/Azure/azure-sdk-for-python/issues/8990
    await keyvault_client.close()
    await resource_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

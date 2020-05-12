# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from dateutil import parser as date_parse

from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import EnvironmentCredential
from azure.keyvault.keys import KeyClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient


# Cerdential for track1 sdk
credential4track1 = ServicePrincipalCredentials(
    client_id=os.environ.get("AZURE_CLIENT_ID"),
    secret=os.environ.get("AZURE_CLIENT_SECRET"),
    tenant=os.environ.get("AZURE_TENANT_ID")
)

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TENANT_ID = os.environ.get("AZURE_TENANT_ID", None)
    DISK_ENCRYPTION_SET_NAME = "diskencryptionsetxxx"
    GROUP_NAME = "testgroupx"
    KEY_VAULT = "keyvaultxyzxxxxx"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # track 1 sdk
    keyvault_client = KeyVaultManagementClient(
        credentials=credential4track1,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create key
    vault = keyvault_client.vaults.create_or_update(
        GROUP_NAME,
        KEY_VAULT,
        {
            'location': "eastus",
            'properties': {
            'sku': {
                'name': 'standard'
            },
            'tenant_id': TENANT_ID,
            "access_policies": [
                {
                "tenant_id": TENANT_ID,
                "object_id": "123743cc-88ef-49ee-920e-13958fe5697d",
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
                    ]
                }
                }
            ],
            'enabled_for_disk_encryption': True,
            }
        }
    ).result()

    key_client = KeyClient(vault.properties.vault_uri, EnvironmentCredential())
    
    expires_on = date_parse.parse("2050-02-02T08:00:00.000Z")

    key = key_client.create_key(
        "testkey",
        "RSA",
        size=2048,
        expires_on=expires_on
    )

    # Create disk encryption set
    encryption_set = compute_client.disk_encryption_sets.begin_create_or_update(
        GROUP_NAME,
        DISK_ENCRYPTION_SET_NAME,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
          },
          "active_key": {
            "source_vault": {
              "id": vault.id
            },
            "key_url": key.id
          }
        }
    ).result()
    print("Create disk encryption set:\n{}".format(encryption_set))

    # Get disk encrytion set
    encryption_set = compute_client.disk_encryption_sets.get(
        GROUP_NAME,
        DISK_ENCRYPTION_SET_NAME
    )
    print("Get disk encryption set:\n{}".format(encryption_set))

    # Update disk encryption set
    encryption_set = compute_client.disk_encryption_sets.begin_update(
        GROUP_NAME,
        DISK_ENCRYPTION_SET_NAME,
        {
          "active_key": {
            "source_vault": {
              "id": vault.id
            },
            "key_url": key.id
          },
          "tags": {
            "department": "Development",
            "project": "Encryption"
          }
        }
    ).result()
    print("Update disk encryption set:\n{}".format(encryption_set))

    # Delete disk encryption set
    compute_client.disk_encryption_sets.begin_delete(
        GROUP_NAME,
        DISK_ENCRYPTION_SET_NAME
    )
    print("Delete disk encryption set.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

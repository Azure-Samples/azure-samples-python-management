# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import base64
import os
import random

from azure.identity import DefaultAzureCredential
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VAULT_EXTENDED_INFO = "vault_extended_infoxxyyzz"
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

    # - init depended resources -
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
    # - end -

    # Create vault extended info
    vault_extended_info = recoveryservices_client.vault_extended_info.create_or_update(
        GROUP_NAME,
        VAULT,
        {
            "algorithm": "None",
            "integrity_key": base64.b64encode(bytearray(random.getrandbits(8) for i in range(16)))
        }
    )
    print("Create vault extended info:\n{}".format(vault_extended_info))

    # Get vault extended info
    vault_extended_info = recoveryservices_client.vault_extended_info.get(
        GROUP_NAME,
        VAULT
    )
    print("Get vault extended info:\n{}".format(vault_extended_info))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

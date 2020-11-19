# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.datalake.store import DataLakeStoreAccountManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datalake.store import models

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testdatalakestore1"
    LOCATION = 'eastus2'

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    datalakestore_client = DataLakeStoreAccountManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": LOCATION}
    )

    # - init depended resources -
    # - end -

    # Create datalakestore
    # define account params
    ACCOUNT_NAME = 'testaccount'

    params_create = models.CreateDataLakeStoreAccountParameters(
        location=LOCATION,
        identity=models.EncryptionIdentity(),
        encryption_config=models.EncryptionConfig(
            type=models.EncryptionConfigType.service_managed
        ),
        encryption_state=models.EncryptionState.enabled,
        tags={
            'tag1': 'value1'
        }
    )

    # params_create_no_encryption = models.CreateDataLakeStoreAccountParameters(
    #     location=location,
    #     tags={
    #         'tag1': 'value1'
    #     }
    # )
    
    datalakestore = datalakestore_client.accounts.begin_create(
        GROUP_NAME,
        ACCOUNT_NAME,
        params_create
    ).result()
    print("Create datalakestore:\n{}".format(datalakestore))

    # Get datalakestore
    datalakestore = datalakestore_client.accounts.get(
        GROUP_NAME,
        ACCOUNT_NAME
    )
    print("Get datalakestore:\n{}".format(datalakestore))

    # Update datalakestore
    datalakestore = datalakestore_client.accounts.begin_update(
        GROUP_NAME,
        ACCOUNT_NAME,
        models.UpdateDataLakeStoreAccountParameters(
                tags={
                    'tag2': 'value2'
                }
            )
    ).result()
    print("Update datalakestore:\n{}".format(datalakestore))
    
    # Delete datalakestore
    datalakestore = datalakestore_client.accounts.begin_delete(
        GROUP_NAME,
        ACCOUNT_NAME
    ).result()
    print("Delete datalakestore.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

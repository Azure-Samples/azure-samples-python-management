# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.relay import RelayAPI
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE = "namespacexxyzx"
    HYBRIDCONNECTION = "hybridconnectionxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    relay_client = RelayAPI(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create namespace
    namespace = relay_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
            "location": "eastus",
            "tags": {
                "tag1": "value1",
                "tag2": "value2"
            },
            "sku": {
                "tier": "standard"
            }
        }
    ).result()
    print("Create namespace:\n{}".format(namespace))
    # - end -

    # Create hybridconnection
    hybridconnection = relay_client.hybrid_connections.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        HYBRIDCONNECTION,
        {
            "requires_client_authorization": True,
            "user_metadata": "User data for HybridConnection"
        }
    )
    print("Create hybridconnection:\n{}".format(hybridconnection))

    # Get hybridconnection
    hybridconnection = relay_client.hybrid_connections.get(
        GROUP_NAME,
        NAMESPACE,
        HYBRIDCONNECTION
    )
    print("Get hybridconnection:\n{}".format(hybridconnection))

    # Delete hybridconnection
    hybridconnection = relay_client.hybrid_connections.delete(
        GROUP_NAME,
        NAMESPACE,
        HYBRIDCONNECTION
    )
    print("Delete hybridconnection.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

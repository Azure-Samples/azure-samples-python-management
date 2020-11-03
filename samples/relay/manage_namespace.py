# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.relay import RelayAPI
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NAMESPACE = "namespacexxyyzz"

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

    # Get namespace
    namespace = relay_client.namespaces.get(
        GROUP_NAME,
        NAMESPACE
    )
    print("Get namespace:\n{}".format(namespace))

    # Update namespace
    namespace = relay_client.namespaces.update(
        GROUP_NAME,
        NAMESPACE,
        {
            "tags": {
                "tag1": "value2"
            }
        }
    )
    print("Update namespace:\n{}".format(namespace))
    
    # Delete namespace
    namespace = relay_client.namespaces.begin_delete(
        GROUP_NAME,
        NAMESPACE
    ).result()
    print("Delete namespace.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

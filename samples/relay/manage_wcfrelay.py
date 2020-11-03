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
    WCFRELAY = "wcfrelayxxyyzz"
    NAMESPACE = "namespacexxyze"

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

    # Create wcfrelay
    wcfrelay = relay_client.wcf_relays.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        WCFRELAY,
        {
            "relay_type": "NetTcp",
            "requires_client_authorization": True,
            "requires_transport_security": True,
            "user_metadata": "User dta for WcfRelay"
        }
    )
    print("Create wcfrelay:\n{}".format(wcfrelay))

    # Get wcfrelay
    wcfrelay = relay_client.wcf_relays.get(
        GROUP_NAME,
        NAMESPACE,
        WCFRELAY
    )
    print("Get wcfrelay:\n{}".format(wcfrelay))

    # Delete wcfrelay
    wcfrelay = relay_client.wcf_relays.delete(
        GROUP_NAME,
        NAMESPACE,
        WCFRELAY
    )
    print("Delete wcfrelay.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

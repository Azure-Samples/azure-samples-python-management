# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TAG_NAME = "tagxyz"
    TAG_VALUE = "value1"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create tag
    tag = resource_client.tags.create_or_update(
        TAG_NAME
    )
    print("Create tag:\n{}".format(tag))

    # Create tag value
    tag = resource_client.tags.create_or_update_value(
        TAG_NAME,
        TAG_VALUE
    )
    print("Create tag value:\n{}".format(tag))

    # Get at scope
    scope = "subscriptions/" + SUBSCRIPTION_ID
    tag = resource_client.tags.get_at_scope(
        scope
    )
    print("Get tag:\n{}".format(tag))

    # Delete tag value
    resource_client.tags.delete_value(
        TAG_NAME,
        TAG_VALUE
    )
    print("Delete tag value:\n")

    # Delete tag
    tag = resource_client.tags.delete(
        TAG_NAME
    )
    print("Delete tag.\n")


if __name__ == "__main__":
    main()

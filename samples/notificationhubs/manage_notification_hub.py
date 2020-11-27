# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time

from azure.identity import DefaultAzureCredential
from azure.mgmt.notificationhubs import NotificationHubsManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NOTIFICATION_HUB = "notification_hubxxyyzz"
    NAMESPACE = "namespacexxyz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    notificationhubs_client = NotificationHubsManagementClient(
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
    namespace = notificationhubs_client.namespaces.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
            "location": "eastus"
        }
    )
    namespace = notificationhubs_client.namespaces.get(
        GROUP_NAME,
        NAMESPACE
    )
    while namespace.status == "Created":
        time.sleep(30)
        namespace = notificationhubs_client.namespaces.get(
            GROUP_NAME,
            NAMESPACE,
        )
    print("Create namespace:\n{}".format(namespace))
    # - end -

    # Create notification hub
    notification_hub = notificationhubs_client.notification_hubs.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        NOTIFICATION_HUB,
        {
            "location": "eastus"
        }
    )
    print("Create notification hub:\n{}".format(notification_hub))

    # Get notification hub
    notification_hub = notificationhubs_client.notification_hubs.get(
        GROUP_NAME,
        NAMESPACE,
        NOTIFICATION_HUB
    )
    print("Get notification hub:\n{}".format(notification_hub))

    # Delete notification hub
    notificationhubs_client.notification_hubs.delete(
        GROUP_NAME,
        NAMESPACE,
        NOTIFICATION_HUB
    )
    print("Delete notification hub.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.subscriptions import SubscriptionClient


def main():
    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    subscription_client = SubscriptionClient(
        credential=DefaultAzureCredential()
    )

    # List subscriptions
    page_result = subscription_client.subscriptions.list()
    result = [item for item in page_result]
    for item in result:
        print(item.subscription_id)
        print(item.tags)


if __name__ == "__main__":
    main()

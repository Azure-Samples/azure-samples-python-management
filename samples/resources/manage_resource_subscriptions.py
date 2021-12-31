# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.subscriptions import SubscriptionClient


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    subscription_client = SubscriptionClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # List subscriptions
    page_result = subscription_client.subscriptions.list()
    result = [item for item in page_result]
    for item in result:
        print(item.subscription_id)


if __name__ == "__main__":
    main()

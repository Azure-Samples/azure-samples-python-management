# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
    client = ResourceManagementClient(credential=DefaultAzureCredential(), subscription_id=SUBSCRIPTION_ID)
    result = client.providers.list()
    for item in result:
        print(item)


if __name__ == "__main__":
    main()

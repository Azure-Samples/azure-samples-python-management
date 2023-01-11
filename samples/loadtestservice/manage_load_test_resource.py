# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: manage_load_test_resource.py

DESCRIPTION:
    This sample shows how to manage Azure Load Testing Resources using python SDK.

USAGE:
    python manage_load_test_resource.py

    Set the environment variables with your values before running the sample:
    1)  AZURE_CLIENT_ID - client id
    2)  AZURE_CLIENT_SECRET - client secret
    3)  AZURE_TENANT_ID - tenant id
    4)  SUBSCRIPTION_ID - subscription id
"""

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.loadtesting import LoadTestMgmtClient
from azure.mgmt.loadtesting.models import (
    LoadTestResource, 
    LoadTestResourcePatchRequestBody, 
    ManagedServiceIdentity
)

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    RESOURCE_GROUP_NAME = "sample-rg"
    RESOURCE_NAME = "sample-loadtesting-resource"
    RESOURCE_LOCATION = "westus2"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    client = LoadTestMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # load test resource creation payload
    loadtestresource_create_payload = LoadTestResource(
        location=RESOURCE_LOCATION
        # Add other properties if needed.
    )

    # Create a load test resource - returns a poller
    poller = client.load_tests.begin_create_or_update(
        RESOURCE_GROUP_NAME, 
        RESOURCE_NAME, 
        loadtestresource_create_payload
    )
        
    # Get the result of the poller
    loadtest_resource = poller.result()

    # Use the newly created load test resource
    print(loadtest_resource.id)

    # Get the details of an existing load test resource
    loadtest_resource = client.load_tests.get(
        RESOURCE_GROUP_NAME, 
        RESOURCE_NAME
    )

    # load test resource update payload
    loadtestresource_update_payload = LoadTestResourcePatchRequestBody(
        identity=ManagedServiceIdentity(
            type="SystemAssigned"
        )
    )

    # load test resource update begin - returns a poller
    poller = client.load_tests.begin_update(
        RESOURCE_GROUP_NAME, 
        RESOURCE_NAME,
        loadtestresource_update_payload
    )
    
    # Get the result of the poller
    loadtest_resource = poller.result()

    # Delete the load test resource
    poller = client.load_tests.begin_delete(
        RESOURCE_GROUP_NAME, 
        RESOURCE_NAME
    )

if __name__ == "__main__":
    main()

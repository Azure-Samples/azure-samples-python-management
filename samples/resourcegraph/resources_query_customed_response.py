# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest


def custom_res(pipeline_response, deserialized, *kwargs):
    resource = deserialized
    quota_remaining = None
    quota_resets_after = None
    try:
        headers = pipeline_response.http_response.internal_response.headers
        quota_remaining = headers._store['x-ms-user-quota-remaining']
        quota_resets_after = headers._store['x-ms-user-quota-resets-after']
    except AttributeError:
        pass
    setattr(resource, 'x-ms-user-quota-remaining', quota_remaining)
    setattr(resource, 'x-ms-user-quota-resets-after', quota_resets_after)
    return resource


def main():
    # If "SUBSCRIPTION_ID" is not set in the environment variable, you need to set it manually: export SUBSCRIPTION_ID="{SUBSCRIPTION_ID}"
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resourcegraph_client = ResourceGraphClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Basic query up to 2 pieces of data
    query = QueryRequest(
        query='project id, tags, properties | limit 2',
        subscriptions=[SUBSCRIPTION_ID]
    )
    query_response = resourcegraph_client.resources(query, cls=custom_res)
    print("Basic query up to 2 pieces of data:\n{}".format(query_response))


if __name__ == "__main__":
    main()

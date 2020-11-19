# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resourcegraph.models import *

# - other dependence -
# - end -
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
    query_response = resourcegraph_client.resources(query)
    print("Basic query up to 2 pieces of data:\n{}".format(query_response))

    # Basic query up to 2 pieces of object array
    query = QueryRequest(
            query='project id, tags, properties | limit 2',
            subscriptions=[SUBSCRIPTION_ID],
            options=QueryRequestOptions(
                result_format=ResultFormat.object_array
            )
        )
    query_response = resourcegraph_client.resources(query)
    print("Basic query up to 2 pieces of object array:\n{}".format(query_response))

    # Query with options
    query = QueryRequest(
            query='project id',
            subscriptions=[SUBSCRIPTION_ID],
            options=QueryRequestOptions(
                top=4,
                skip=8
            )
        )
    query_response = resourcegraph_client.resources(query)
    print("Query with options:\n{}".format(query_response))

    # Query with facet expressions
    facet_expression0 = 'location'
    facet_expression1 = 'nonExistingColumn'

    query = QueryRequest(
        query='project id, location | limit 10',
        subscriptions=[SUBSCRIPTION_ID],
        facets=[
            FacetRequest(
                expression=facet_expression0,
                options=FacetRequestOptions(
                    sort_order='desc',
                    top=1
                )
            ),
            FacetRequest(
                expression=facet_expression1,
                options=FacetRequestOptions(
                    sort_order='desc',
                    top=1
                )
            )
        ]
    )
    query_response = resourcegraph_client.resources(query)
    print("Query with facet expressions:\n{}".format(query_response))


if __name__ == "__main__":
    main()

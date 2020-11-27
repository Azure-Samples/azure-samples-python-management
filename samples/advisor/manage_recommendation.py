# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import re

from azure.identity import DefaultAzureCredential
from azure.mgmt.advisor import AdvisorManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    RECOMMENDATION = "recommendationxxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    advisor_client = AdvisorManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    def call(response, *args, **kwargs):
        return response.http_response

    # Generate recommendation
    response = advisor_client.recommendations.generate(cls=call)

    location = response.headers['Location']
    # extract the operation ID from the Location header
    operation_id = re.findall("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", location)

    # Get generate status 
    recommendation = advisor_client.recommendations.get_generate_status(
        cls=call,
        operation_id=operation_id[0]
    )
    print("Get recommendation status:\n{}".format(recommendation))


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.','')
    GROUP_NAME = "testeventgrid" + TIME
    EVENTGRID = "eventgrid" + TIME
    LOCATION='eastus'

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    eventgrid_client = EventGridManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": LOCATION}
    )

    # - init depended resources -
    # - end -

    # Create eventgrid
    eventgrid = eventgrid_client.domains.begin_create_or_update(
        GROUP_NAME,
        EVENTGRID,
        {
            "location":LOCATION
        }
    ).result()
    print("Create eventgrid:\n{}".format(eventgrid))

    # Get eventgrid
    eventgrid = eventgrid_client.domains.get(
        GROUP_NAME,
        EVENTGRID
    )
    print("Get eventgrid:\n{}".format(eventgrid))

    # Update eventgrid
    eventgrid = eventgrid_client.domains.begin_update(
        GROUP_NAME,
        EVENTGRID,
        {
            "tags": {
                "tag1": "value1",
                "tag2": "value2"
            }
        }
    ).result()
    print("Update eventgrid:\n{}".format(eventgrid))
    
    # Delete eventgrid
    eventgrid_client.domains.begin_delete(
        GROUP_NAME,
        EVENTGRID
    ).result()
    print("Delete eventgrid.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

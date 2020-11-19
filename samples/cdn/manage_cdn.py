# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.cdn import CdnManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.','')
    GROUP_NAME = "testcdn" + TIME
    CDN = "cdn" + TIME
    LOCATION='WestUs'

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    cdn_client = CdnManagementClient(
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

    # Create cdn
    cdn = cdn_client.profiles.begin_create(
        GROUP_NAME,
        CDN,
        {
            "location": LOCATION,
            "sku": {
                "name": "Standard_Verizon"
            }
        }
    ).result()
    print("Create cdn:\n{}\n".format(cdn))

    # Get cdn
    cdn = cdn_client.profiles.get(
        GROUP_NAME,
        CDN
    )
    print("Get cdn:\n{}\n".format(cdn))

    # Update cdn
    cdn = cdn_client.profiles.begin_update(
        GROUP_NAME,
        CDN,
        {
            "tags": {
                "additional_properties": "Tag1"
            }
        }
    ).result()
    print("Update cdn:\n{}\n".format(cdn))
    
    # Delete cdn
    cdn = cdn_client.profiles.begin_delete(
        GROUP_NAME,
        CDN
    ).result()
    print("Delete cdn.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

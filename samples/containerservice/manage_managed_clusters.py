# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.resource import ResourceManagementClient


# - other dependence -
# - end -


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    CLIENT_ID = os.environ.get("CLIENT_ID", None)
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
    GROUP_NAME = "testgroupx"
    MANAGED_CLUSTERS = "managed_clustersxxyyzz"
    AZURE_LOCATION = "eastus"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    containerservice_client = ContainerServiceClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": AZURE_LOCATION}
    )

    # - init depended resources -
    # - end -

    # Create managed clusters
    managed_clusters = containerservice_client.managed_clusters.begin_create_or_update(
        GROUP_NAME,
        MANAGED_CLUSTERS,
        {
            "dns_prefix": "akspythonsdk",
            "agent_pool_profiles": [
                {
                    "name": "aksagent",
                    "count": 1,
                    "vm_size": "Standard_DS2_v2",
                    "max_pods": 110,
                    "min_count": 1,
                    "max_count": 100,
                    "os_type": "Linux",
                    "type": "VirtualMachineScaleSets",
                    "enable_auto_scaling": True,
                    "mode": "System",
                }
            ],
            "service_principal_profile": {
                "client_id": CLIENT_ID,
                "secret": CLIENT_SECRET
            },
            "location": AZURE_LOCATION
        }
    ).result()
    print("Create managed clusters:\n{}".format(managed_clusters))

    # Get managed clusters
    managed_clusters = containerservice_client.managed_clusters.get(
        GROUP_NAME,
        MANAGED_CLUSTERS
    )
    print("Get managed clusters:\n{}".format(managed_clusters))

    # Update managed clusters
    managed_clusters = containerservice_client.managed_clusters.begin_update_tags(
        GROUP_NAME,
        MANAGED_CLUSTERS,
        {
            "tags": {
                "tier": "testing",
                "archv3": ""
            }
        }
    ).result()
    print("Update managed clusters:\n{}".format(managed_clusters))

    # Delete managed clusters
    managed_clusters = containerservice_client.managed_clusters.begin_delete(
        GROUP_NAME,
        MANAGED_CLUSTERS
    ).result()
    print("Delete managed clusters.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

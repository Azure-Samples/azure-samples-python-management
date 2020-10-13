# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.resource import ResourceManagementClient


# - other dependence -
# - end -


def main():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    AGENT_POOL = "agent_poolxxyyzz"
    AGENT_POOL_NAME = "aksagent"
    CLIENT_ID = os.environ.get("CLIENT_ID", None)
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
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
        AGENT_POOL,
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
    # Create agent pool
    for i in range(10):
        try:
            agent_pool = containerservice_client.agent_pools.begin_create_or_update(
                GROUP_NAME,
                AGENT_POOL,
                AGENT_POOL_NAME,
                {
                    "orchestrator_version": "",
                    "count": "3",
                    "vm_size": "Standard_DS2_v2",
                    "os_type": "Linux",
                    "type": "VirtualMachineScaleSets",
                    "mode": "System",
                    "availability_zones": [
                        "1",
                        "2",
                        "3"
                    ],
                    "node_taints": []
                }
            ).result()
        except:
            time.sleep(30)
        else:
            break
    print("Create agent pool:\n{}".format(agent_pool))

    # Get agent pool
    agent_pool = containerservice_client.agent_pools.get(
        GROUP_NAME,
        AGENT_POOL,
        AGENT_POOL_NAME
    )
    print("Get agent pool:\n{}".format(agent_pool))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

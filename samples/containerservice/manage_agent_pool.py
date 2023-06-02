# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerservice import models
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv


def main():
    load_dotenv()
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    MANAGED_CLUSTERS = "managed_clustersxxyyzz"
    AGENT_POOL_NAME = "aksagent"
    CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", None)
    CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", None)
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

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": AZURE_LOCATION}
    )

    # Create managed clusters
    managed_clusters = containerservice_client.managed_clusters.begin_create_or_update(
        GROUP_NAME,
        MANAGED_CLUSTERS,
        parameters=models.ManagedCluster(
            dns_prefix="akspythonsdk",
            agent_pool_profiles=[models.ManagedClusterAgentPoolProfile(
                name="aksagent", min_count=1, max_count=3, count=2,
                vm_size="Standard_DS2_v2",
                max_pods=50, os_type="Linux", type="VirtualMachineScaleSets",
                enable_auto_scaling=True, mode="System")],
            service_principal_profile=models.ManagedClusterServicePrincipalProfile(client_id=CLIENT_ID,
                                                                                   secret=CLIENT_SECRET),
            location=AZURE_LOCATION
        ),
    ).result()
    print("Create managed clusters:\n{}".format(managed_clusters.serialize()))

    # Create agent pool
    agent_pool = containerservice_client.agent_pools.begin_create_or_update(
        GROUP_NAME,
        MANAGED_CLUSTERS,
        AGENT_POOL_NAME,
        parameters=models.AgentPool(
            max_count=10, min_count=1, vm_size="Standard_DS2_v2", os_type="Linux", enable_auto_scaling=True,
            type_properties_type="VirtualMachineScaleSets", mode="System",
            availability_zones=["1", "2", "3"])
    ).result()
    print("Create agent pool:\n{}".format(agent_pool.serialize()))

    # Get agent pool
    agent_pool = containerservice_client.agent_pools.get(
        GROUP_NAME,
        MANAGED_CLUSTERS,
        AGENT_POOL_NAME
    )
    print("Get agent pool:\n{}".format(agent_pool.serialize()))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

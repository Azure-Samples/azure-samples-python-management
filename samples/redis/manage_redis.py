# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    REDIS = "redisxxyyzz"
    NETWORK_NAME = "networknamex"
    SUBNET_NAME = "subnetnamex"


    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    redis_client = RedisManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    ).result()

    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    ).result()

    # Create redis
    redis = redis_client.redis.begin_create(
        GROUP_NAME,
        REDIS,
        {
          "location": "eastus",
          "zones": [
            "1"
          ],
          "sku": {
            "name": "Premium",
            "family": "P",
            "capacity": "1"
          },
          "enable_non_ssl_port": True,
          "shard_count": "2",
          # "replicas_per_master": "2",
          "redis_configuration": {
            "maxmemory-policy": "allkeys-lru"
          },
          "subnet_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + NETWORK_NAME + "/subnets/" + SUBNET_NAME,
          "static_ip": "10.0.0.5",
          "minimum_tls_version": "1.2"
        }
    ).result()
    print("Create redis:\n{}".format(redis))

    # Get redis
    redis = redis_client.redis.get(
        GROUP_NAME,
        REDIS
    )
    print("Get redis:\n{}".format(redis))

    # Update redis
    redis = redis_client.redis.update(
        GROUP_NAME,
        REDIS,
        {
            "enable_non_ssl_port": True
        }
    )
    print("Update redis:\n{}".format(redis))
    
    # Delete redis
    redis = redis_client.redis.begin_delete(
        GROUP_NAME,
        REDIS
    ).result()
    print("Delete redis.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()


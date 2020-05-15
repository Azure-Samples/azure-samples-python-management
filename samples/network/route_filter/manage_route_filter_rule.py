# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ROUTE_FILTER_RULE = "route_filter_rulexxyyzz"
    ROUTE_FILTER = "route_filterxxyyzz"

    # Create client
    resource_client = ResourceManagementClient(
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

    # - init depended resources -
    # Create route filter
    network_client.route_filters.begin_create_or_update(
        GROUP_NAME,
        ROUTE_FILTER,
        {
          "location": "eastus",
          "tags": {
            "key1": "value1"
          },
          "rules": []
        }
    ).result()
    # - end -

    # Create route filter rule
    route_filter_rule = network_client.route_filter_rules.begin_create_or_update(
        GROUP_NAME,
        ROUTE_FILTER,
        ROUTE_FILTER_RULE,
        {
          "access": "Allow",
          "route_filter_rule_type": "Community",
          "communities": [
            "12076:51004"
          ]
        }
    ).result()
    print("Create route filter rule:\n{}".format(route_filter_rule))

    # Get route filter rule
    route_filter_rule = network_client.route_filter_rules.get(
        GROUP_NAME,
        ROUTE_FILTER,
        ROUTE_FILTER_RULE
    )
    print("Get route filter rule:\n{}".format(route_filter_rule))

    # Delete route filter rule
    route_filter_rule = network_client.route_filter_rules.begin_delete(
        GROUP_NAME,
        ROUTE_FILTER,
        ROUTE_FILTER_RULE
    ).result()
    print("Delete route filter rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

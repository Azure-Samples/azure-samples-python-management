# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.advisor import AdvisorManagementClient
from azure.mgmt.advisor.models import ConfigData
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    CONFIGURATION = "default"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    advisor_client = AdvisorManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # create a new configuration to update exclude to True
    input = ConfigData()
    input.exclude=True

    # Create configuration
    configuration = advisor_client.configurations.create_in_resource_group(
        configuration_name=CONFIGURATION,
        resource_group=GROUP_NAME,
        config_contract=input
    )
    print("Create configuration:\n{}".format(configuration))

    # Get configuration
    configurations = advisor_client.configurations.list_by_resource_group(
        resource_group=GROUP_NAME,
    )
    print("Get configuration:\n{}".format(list(configurations)[0]))

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

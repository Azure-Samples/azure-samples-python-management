# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredentials 
from azure.mgmt.msi import ManagedServiceIdentityClient
from azure.mgmt.resource import DeploymentScriptsClient, ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    IDENTITY_NAME = "uai"
    SCRIPT_NAME = "scriptxx"

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    script_client = DeploymentScriptsClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    msi_client = ManagedServiceIdentityClient(
        credentials=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create identity
    msi_client.user_assigned_identities.create_or_update(
        GROUP_NAME,
        IDENTITY_NAME,
        "westus",
        {"key1": "value1"}
    )

    # Create script
    # azure.core.exceptions.HttpResponseError: Operation returned an invalid status 'OK'
    script_client.deployment_scripts.begin_create(
        GROUP_NAME,
        SCRIPT_NAME,
        {
            "kind": "AzurePowerShell",
            "location": "westus",
            "identity": {
                "type": "UserAssigned",
                "user_assigned_identities": {
                    "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.ManagedIdentity/userAssignedIdentities/" + IDENTITY_NAME: {}
                }
            },
            "azPowerShellVersion": "3.0",
            "scriptContent": "Param([string]$Location,[string]$Name) $deploymentScriptOutputs['test'] = 'value' Get-AzResourceGroup -Location $Location -Name $Name",
            "arguments": "-Location 'westus' -Name \"*rg2\"",
            "retentionInterval": "P7D",
            "timeout": "PT1H",
            "cleanupPreference": "Always"
        }
    ).result()
    print("Create script.\n")

    # Update script
    script = script_client.deployment_scripts.update(
        GROUP_NAME,
        SCRIPT_NAME,
        {
            "tags": {"key1": "value1"}
        }
    )
    print("Update script:\n{}".format(script))

    # Get script
    script = script_client.deployment_scripts.get(
        GROUP_NAME,
        SCRIPT_NAME
    )
    print("Get script:\n{}".format(script))

    # Get script logs
    script_logs = script_client.deployment_scripts.get_logs(
        GROUP_NAME,
        SCRIPT_NAME
    )
    print("Get script logs:\n{}".format(script_logs))

    # Delete script
    script_client.deployment_scripts.delete(
        GROUP_NAME,
        SCRIPT_NAME
    )
    print("Delete script.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

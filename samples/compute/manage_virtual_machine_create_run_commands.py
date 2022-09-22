# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# reference with https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command-managed#execute-a-script-with-the-vm
def main():
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    GROUP_NAME = "vm-run-command"  # you need to create it before run the file
    VIRTUAL_MACHINE_NAME = "vm-run-command"  # you need to create it before run the file
    LOCATION = 'eastus'

    compute_client = ComputeManagementClient(DefaultAzureCredential(), SUBSCRIPTION_ID)
    create_result = compute_client.virtual_machine_run_commands.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME,
        run_command_name='remove-unexisting-files3',
        run_command={
            "location": LOCATION,
            "properties": {
                "source": {
                    'commandId': 'RunShellScript',
                    'script': [
                        'cd /home',
                        'rm -rf /no-existing/folder'
                    ]
                },
                "timeoutInSeconds": 10000,
            }
        }
    ).result()
    result = list(compute_client.virtual_machine_run_commands.list_by_virtual_machine(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME
    ))
    for item in result:
        print(item)

if __name__ == "__main__":
    main()

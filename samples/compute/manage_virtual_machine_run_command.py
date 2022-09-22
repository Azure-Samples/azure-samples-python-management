# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# reference with https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command#azure-cli
def main():
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    GROUP_NAME = "vm-run-command"  # you need to create it before run the file
    VIRTUAL_MACHINE_NAME = "vm-run-command"  # you need to create it before run the file

    compute_client = ComputeManagementClient(DefaultAzureCredential(), SUBSCRIPTION_ID)
    result = compute_client.virtual_machines.begin_run_command(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME,
        parameters={
            'commandId': 'RunShellScript',
            'script': [
                'cd /home',
                'mkdir for-test'
            ]
        }
    ).result()
    for item in result.value:
      print(item.message)

if __name__ == "__main__":
    main()

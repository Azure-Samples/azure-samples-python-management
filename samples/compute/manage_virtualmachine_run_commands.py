import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('AZURE_SUBSCRIPTION_ID')

    compute_client = ComputeManagementClient(credentials, subscription)

    GROUP_NAME = "testgroup"
    SSH_PUBLIC_KEY_NAME = "keyname"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"
    RUN_COMMAND_NAME = "testrun"
    LOCATION = 'eastus'
    UserName = 'azureuser'

    ssh_key = compute_client.ssh_public_keys.get(
        resource_group_name=GROUP_NAME,
        ssh_public_key_name=SSH_PUBLIC_KEY_NAME
    ).public_key
    print(ssh_key)

    result = compute_client.virtual_machine_run_commands.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME,
        run_command_name=RUN_COMMAND_NAME,
        run_command={
            "location": LOCATION,
            "properties": {
                "source": {
                    'script': [
                        'Write-Host Hello World!'
                    ]
                },
                "parameters": [
                    {
                        "name": "arg1",
                        "value": "hello world"
                    },
                    {
                        "name": "arg2",
                        "value": "Hallo World hhhhhhhh"
                    }
                ],
                "runAsUser": UserName,
                "runAsPassword": ssh_key,
                "timeoutInSeconds": 10,
            }
        }
    ).result()
    print(result)


if __name__ == '__main__':
    main()

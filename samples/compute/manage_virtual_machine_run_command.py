import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('AZURE_SUBSCRIPTION_ID')

    compute_client = ComputeManagementClient(credentials, subscription)

    GROUP_NAME = "testgroupx"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"

    result = compute_client.virtual_machines.begin_run_command(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME,
        parameters={
            'command_id': 'RunShellScript',
            'script': [
                'echo $arg1'
            ],
            'parameters': [
                {'name': "arg1", 'value': "hello world"}
            ]
        }
    ).result()
    print(result.value[0].message)


if __name__ == '__main__':
    main()

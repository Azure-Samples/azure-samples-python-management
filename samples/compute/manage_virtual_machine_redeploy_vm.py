import os
import random
import string

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"
    INTERFACE_NAME = "interfacex"

    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )
    # Create virtual machine
    vm = compute_client.virtual_machines.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        {
            "location": "eastus",
            "hardware_profile": {
                "vm_size": "Standard_D2_v2"
            },
            "storage_profile": {
                "image_reference": {
                    "sku": "2016-Datacenter",
                    "publisher": "MicrosoftWindowsServer",
                    "version": "latest",
                    "offer": "WindowsServer"
                },
                "os_disk": {
                    "caching": "ReadWrite",
                    "managed_disk": {
                        "storage_account_type": "Standard_LRS"
                    },
                    "name": "myVMosdisk",
                    "create_option": "FromImage"
                },
                "data_disks": [
                    {
                        "disk_size_gb": "1023",
                        "create_option": "Empty",
                        "lun": "0"
                    },
                    {
                        "disk_size_gb": "1023",
                        "create_option": "Empty",
                        "lun": "1"
                    }
                ]
            },
            "os_profile": {
                "admin_username": "testuser",
                "computer_name": "myVM",
                "admin_password": your_password,
                "windows_configuration": {
                    "enable_automatic_updates": True  # need automatic update for reimage
                }
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + INTERFACE_NAME + "",
                        # "id": NIC_ID,
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            }
        }
    ).result()
    print("Create virtual machine:\n{}".format(vm))

    # redeploy vm
    result = compute_client.virtual_machines.begin_redeploy(
        resource_group_name=GROUP_NAME,
        vm_name=VIRTUAL_MACHINE_NAME
    ).result()
    print(result)

    compute_client.virtual_machines.begin_delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    ).result()
    print("Delete virtual machine.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == '__main__':
    main()

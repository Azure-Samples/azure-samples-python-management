# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os
import random
import string

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.compute.aio import ComputeManagementClient
from azure.mgmt.network.aio import NetworkManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"
    SUBNET_NAME = "subnetx"
    INTERFACE_NAME = "interfacex"
    NETWORK_NAME = "networknamex"
    VIRTUAL_MACHINE_EXTENSION_NAME = "virtualmachineextensionx"

    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create virtual network
    await network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )

    subnet = await network_client.subnets.create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )

    # Create network interface
    await network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        INTERFACE_NAME,
        {
            'location': "eastus",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': subnet.id
                }
            }]
        } 
    )

    # Create virtual machine
    vm = await compute_client.virtual_machines.create_or_update(
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
                    "properties": {
                    "primary": True
                    }
                }
                ]
            }
        }
    )
    print("Create virtual machine:\n{}".format(vm))

    # Create vm extension
    extension = await compute_client.virtual_machine_extensions.create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME,
        {
        "location": "eastus",
        "auto_upgrade_minor_version": True,
        "publisher": "Microsoft.Azure.NetworkWatcher",
        "type_properties_type": "NetworkWatcherAgentWindows",  # TODO: Is this a bug?
        "type_handler_version": "1.4",
        }
    )
    print("Create vm extension:\n{}".format(extension))

    # Get virtual machine
    vm = await compute_client.virtual_machines.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    )
    print("Get virtual machine:\n{}".format(vm))

    # List virtual machine (List operation will return asyncList)
    vms = list()
    async for vm in compute_client.virtual_machines.list(GROUP_NAME):
        vms.append(vm)
    print("List virtual machine:\n{}".format(vms))

    # Get vm extension
    extension = await compute_client.virtual_machine_extensions.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME
    )
    print("Get vm extesnion:\n{}".format(extension))

    # Update virtual machine
    vm = await compute_client.virtual_machines.update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        {
        "network_profile": {
            "network_interfaces": [
            {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + INTERFACE_NAME + "",
                "properties": {
                "primary": True
                }
            }
            ]
        }
        }
    )
    print("Update virtual machine:\n{}".format(vm))

    # Update vm extension
    extension = await compute_client.virtual_machine_extensions.update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME,
        {
            "auto_upgrade_minor_version": True,
            "instance_view": {
                "name": VIRTUAL_MACHINE_EXTENSION_NAME,
                "type": "CustomScriptExtension"
            }
        }
    )
    print("Update vm extension:\n{}".format(extension))


    # Delete vm extension (Need vm started)
    await compute_client.virtual_machines.start(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    )

    await compute_client.virtual_machine_extensions.delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME
    )
    print("Delete vm extension.\n")

    # Delete virtual machine
    await compute_client.virtual_machines.power_off(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    )

    await compute_client.virtual_machines.delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    )
    print("Delete virtual machine.\n")

    # Delete Group
    await resource_client.resource_groups.delete(
        GROUP_NAME
    )

    await resource_client.close()
    await compute_client.close()
    await network_client.close()
    await credential.close()


if __name__ == "__main__":

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"
    SUBNET_NAME = "subnetx"
    INTERFACE_NAME = "interfacex"
    NETWORK_NAME = "networknamex"
    VIRTUAL_MACHINE_EXTENSION_NAME = "virtualmachineextensionx"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=EnvironmentCredential(),
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

    # Create network interface
    network_client.network_interfaces.begin_create_or_update(
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
    ).result()

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
            "admin_password": "Aa1!zyx_",
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

    # Create vm extension
    extension = compute_client.virtual_machine_extensions.begin_create_or_update(
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
    ).result()
    print("Create vm extension:\n{}".format(extension))

    # Get virtual machine
    vm = compute_client.virtual_machines.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    )
    print("Get virtual machine:\n{}".format(vm))

    # Get vm extension
    extension = compute_client.virtual_machine_extensions.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME
    )
    print("Get vm extesnion:\n{}".format(extension))

    # Update virtual machine
    vm = compute_client.virtual_machines.begin_update(
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
    ).result()
    print("Update virtual machine:\n{}".format(vm))

    # Update vm extension
    extension = compute_client.virtual_machine_extensions.begin_update(
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
    ).result()
    print("Update vm extension:\n{}".format(extension))


    # Delete vm extension (Need vm started)
    compute_client.virtual_machines.begin_start(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    ).result()

    compute_client.virtual_machine_extensions.begin_delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME
    ).result()
    print("Delete vm extension.\n")

    # Delete virtual machine
    compute_client.virtual_machines.begin_power_off(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    ).result()

    compute_client.virtual_machines.begin_delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME
    ).result()
    print("Delete virtual machine.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

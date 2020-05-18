# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    PACKET_CAPTURE = "packet_capturexxyyzz"
    VIRTUAL_MACHINE_NAME = "virtualmachinexx"
    VIRTUAL_NETWORK_NAME = "virtualnetworkxx"
    SUBNET_NAME = "subnetxxx"
    NIC_NAME = "interfacexxx"
    VM_EXTENSION_NAME = "extensionxxx"
    STORAGE_ACCOUNT_NAME = "storageaccountxxxy"
    NETWORK_WATCHER_NAME = "networkwatcher"

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    ).result() 

    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    ).result()

    # Create network interface
    interface = network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        NIC_NAME,
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
    compute_client.virtual_machines.begin_create_or_update(
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
            }
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
                "id": interface.id,
                "properties": {
                  "primary": True
                }
              }
            ]
          }
        }
    ).result()

    # Create vm extension
    compute_client.virtual_machine_extensions.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VM_EXTENSION_NAME,
        {
          "location": "eastus",
          "auto_upgrade_minor_version": True,
          "publisher": "Microsoft.Azure.NetworkWatcher",
          "type_properties_type": "NetworkWatcherAgentWindows",  # TODO: something needs to be fix in compute sdk
          "type_handler_version": "1.4",
        }
    ).result()

    # Create storage account
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            "sku": {
                "name": "Standard_LRS",
            },
            "kind": "Storage",
            "location": "eastus"
        }
    ).result()

    # Create network watcher
    network_client.network_watchers.create_or_update(
        GROUP_NAME,
        NETWORK_WATCHER_NAME,
        {
            "location": "eastus"
        }
    )
    # - end -

    # Create packet capture
    packet_capture = network_client.packet_captures.begin_create(
        GROUP_NAME,
        NETWORK_WATCHER_NAME,
        PACKET_CAPTURE,
        {
          "target": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME + "",
          "storage_location": {
            "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME + "",
            "storage_path": "https://" + STORAGE_ACCOUNT_NAME + ".blob.core.windows.net/capture/pc1.cap",
          }
        }
    ).result()
    print("Create packet capture:\n{}".format(packet_capture))

    # Get packet capture
    packet_capture = network_client.packet_captures.get(
        GROUP_NAME,
        NETWORK_WATCHER_NAME,
        PACKET_CAPTURE
    )
    print("Get packet capture:\n{}".format(packet_capture))

    # Delete packet capture
    packet_capture = network_client.packet_captures.begin_delete(
        GROUP_NAME,
        NETWORK_WATCHER_NAME,
        PACKET_CAPTURE
    ).result()
    print("Delete packet capture.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

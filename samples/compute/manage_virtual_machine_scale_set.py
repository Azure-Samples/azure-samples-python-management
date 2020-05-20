# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import random
import string

from azure.identity import DefaultAzureCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    VIRTUAL_MACHINE_SCALE_SET_NAME = "virtualmachinescaleset"
    VMSS_EXTENSION_NAME = "vmssextensionxx"
    NETWORK_NAME = "networknamex"
    SUBNET_NAME = "subnetnamex"

    your_password = ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredentials(),
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

    # Create virtual machine scale set
    vmss = compute_client.virtual_machine_scale_sets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        {
          "sku": {
            "tier": "Standard",
            "capacity": "2",
            "name": "Standard_D1_v2"
          },
          "location": "eastus",
          "overprovision": True,
          "virtual_machine_profile": {
            "storage_profile": {
              "image_reference": {
                  "offer": "UbuntuServer",
                  "publisher": "Canonical",
                  "sku": "18.04-LTS",
                  "version": "latest"
              },
              "os_disk": {
                "caching": "ReadWrite",
                "managed_disk": {
                  "storage_account_type": "Standard_LRS"
                },
                "create_option": "FromImage",
                "disk_size_gb": "512"
              },
            },
            "os_profile": {
              "computer_name_prefix": "testPC",
              "admin_username": "testuser",
              "admin_password": "Aa!1()-xyz"
            },
            "network_profile": {
              "network_interface_configurations": [
                {
                  "name": "testPC",
                  "primary": True,
                  "enable_ipforwarding": True,
                  "ip_configurations": [
                    {
                      "name": "testPC",
                      "properties": {
                        "subnet": {
                          "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + NETWORK_NAME + "/subnets/" + SUBNET_NAME + ""
                        }
                      }
                    }
                  ]
                }
              ]
            }
          },
          "upgrade_policy": {
            "mode": "Manual"
          },
          "upgrade_mode": "Manual"
        }
    ).result()
    print("Create virtual machine scale set:\n{}".format(vmss))

    # Create vmss extension
    extension = compute_client.virtual_machine_scale_set_extensions.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        VMSS_EXTENSION_NAME,
        {
          "location": "eastus",
          "auto_upgrade_minor_version": True,
          "publisher": "Microsoft.Azure.NetworkWatcher",
          "type_properties_type": "NetworkWatcherAgentWindows",
          "type_handler_version": "1.4",
        }
    ).result()
    print("Create vmss extension:\n{}".format(extension))

    # Get virtual machine scale set
    vmss = compute_client.virtual_machine_scale_sets.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME
    )
    print("Get virtual machine scale set:\n{}".format(vmss))

    # Get vmss extesnion
    extension = compute_client.virtual_machine_scale_set_extensions.get(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        VMSS_EXTENSION_NAME
    )
    print("Get vmss extension:\n{}".format(extension))

    # Update virtual machine scale set
    vmss = compute_client.virtual_machine_scale_sets.begin_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        {
          "sku": {
            "tier": "Standard",
            "capacity": "2",
            "name": "Standard_D1_v2"
          },
          "upgrade_policy": {
            "mode": "Manual"
          }
        }
    ).result()
    print("Update virtual machine scale set:\n{}".format(vmss))

    # Update vmss extension
    extension = compute_client.virtual_machine_scale_set_extensions.begin_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        VMSS_EXTENSION_NAME,
        {
          "auto_upgrade_minor_version": True,
        }
    ).result()
    print("Update vmss extension:\n{}".format(extension))

    # Delete vmss extension
    compute_client.virtual_machine_scale_set_extensions.begin_delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME,
        VMSS_EXTENSION_NAME
    ).result()
    print("Delete vmss extension.\n")

    # Delete virtual machine scale set
    compute_client.virtual_machine_scale_sets.begin_delete(
        GROUP_NAME,
        VIRTUAL_MACHINE_SCALE_SET_NAME
    ).result()
    print("Delete virtual machine scale set.\n")


    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

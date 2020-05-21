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
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NETWORK_NAME = "networkx"
    SUBNET_NAME = "subnetx"
    INTERFACE_NAME = "interfacex"
    VMSS_NAME = "vmssxyz"
    AUTOSCALESETTING_NAME = "autoscalesettingx"

    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
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

    # Create vmss
    vmss = compute_client.virtual_machine_scale_sets.begin_create_or_update(
        GROUP_NAME,
        VMSS_NAME,
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
              }
            },
            "os_profile": {
              "computer_name_prefix": "testPC",
              "admin_username": "testuser",
              "admin_password": your_password
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
                          "id": subnet.id
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

    # Create autoscale setting
    autoscale_setting = monitor_client.autoscale_settings.create_or_update(
        GROUP_NAME,
        AUTOSCALESETTING_NAME,
        {
          "location": "West US",
          "profiles": [
            {
              "name": "adios",
              "capacity": {
                "minimum": "1",
                "maximum": "10",
                "default": "1"
              },
              "rules": [
              ]
            }
          ],
          "enabled": True,
          "target_resource_uri": vmss.id,
          "notifications": [
            {
              "operation": "Scale",
              "email": {
                "send_to_subscription_administrator": True,
                "send_to_subscription_co_administrators": True,
                "custom_emails": [
                  "gu@ms.com",
                  "ge@ns.net"
                ]
              },
              "webhooks": [
              ]
            }
          ]
        }
    )
    print("Create autoscale setting:\n{}".format(autoscale_setting))

    # Get autoscale setting
    autoscale_setting = monitor_client.autoscale_settings.get(
        GROUP_NAME,
        AUTOSCALESETTING_NAME
    )

    # Update autoscale setting
    autoscale_setting = monitor_client.autoscale_settings.update(
        GROUP_NAME,
        AUTOSCALESETTING_NAME,
        {
          "location": "West US",
          "profiles": [
            {
              "name": "adios",
              "capacity": {
                "minimum": "1",
                "maximum": "10",
                "default": "1"
              },
              "rules": [
              ]
            }
          ],
          "enabled": True,
          "target_resource_uri": vmss.id,
          "notifications": [
            {
              "operation": "Scale",
              "email": {
                "send_to_subscription_administrator": True,
                "send_to_subscription_co_administrators": True,
                "custom_emails": [
                  "gu@ms.com",
                  "ge@ns.net"
                ]
              },
              "webhooks": [
              ]
            }
          ]
        }
    )
    print("Update autoscale setting:\n{}".format(autoscale_setting))

    # Delete autoscale setting
    monitor_client.autoscale_settings.delete(
        GROUP_NAME,
        AUTOSCALESETTING_NAME
    )
    print("Delete autoscale setting.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

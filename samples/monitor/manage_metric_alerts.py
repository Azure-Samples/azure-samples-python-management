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
    METRIC_ALERT_NAME = "metricnamexx"
    VM_NAME = "vm_name"
    NETWORK_NAME = "networkxx"
    SUBNET_NAME = "subnetx"
    INTERFACE_NAME = "interfacexx"

    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
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
    monitor_client = MonitorClient(
        credential=DefaultAzureCredentials(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create virtual network
    vnet = network_client.virtual_networks.begin_create_or_update(
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
    interface = network_client.network_interfaces.begin_create_or_update(
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

    # Create vm
    vm = compute_client.virtual_machines.begin_create_or_update(
        GROUP_NAME,
        VM_NAME,
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
                "id": interface.id,
                "properties": {
                  "primary": True
                }
              }
            ]
          }
        }
    ).result()

    RESOURCE_URI = vm.id

    # Create metric alert
    metric_alert = monitor_client.metric_alerts.create_or_update(
        GROUP_NAME,
        METRIC_ALERT_NAME,
        {
          "location": "global",
          "description": "This is the description of the rule1",
          "severity": "3",
          "enabled": True,
          "scopes": [
            RESOURCE_URI
          ],
          "evaluation_frequency": "PT1M",
          "window_size": "PT15M",
          "target_resource_type": "Microsoft.Compute/virtualMachines",
          "target_resource_region": "southcentralus",
          "criteria": {
            "odata.type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria",
            "all_of": [
              {
                "criterion_type": "DynamicThresholdCriterion",
                "name": "High_CPU_80",
                "metric_name": "Percentage CPU",
                "metric_namespace": "microsoft.compute/virtualmachines",
                "operator": "GreaterOrLessThan",
                "time_aggregation": "Average",
                "dimensions": [],
                "alert_sensitivity": "Medium",
                "failing_periods": {
                  "number_of_evaluation_periods": "4",
                  "min_failing_periods_to_alert": "4"
                },
              }
            ]
          },
          "auto_mitigate": False,
          "actions": [
          ]
        }
    )
    print("Create metric alert:\n{}".format(metric_alert))

    # Get metric alert
    metric_alert = monitor_client.metric_alerts.get(
        GROUP_NAME,
        METRIC_ALERT_NAME
    )
    print("Get metric alert:\n{}".format(metric_alert))

    # Delete metric alert
    monitor_client.metric_alerts.delete(
        GROUP_NAME,
        METRIC_ALERT_NAME
    )
    print("Delete metric alert.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

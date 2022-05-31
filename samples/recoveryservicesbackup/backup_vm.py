import os
import random
import re
import string

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.recoveryservicesbackup.activestamp import RecoveryServicesBackupClient
from azure.mgmt.recoveryservicesbackup.activestamp.models import BackupRequestResource, BackupRequest, \
    ProtectedItemResource
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient


credential = DefaultAzureCredential()

SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
recovery_services_client = RecoveryServicesClient(credential, SUBSCRIPTION_ID)
recovery_services_backup_client = RecoveryServicesBackupClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

GROUP_NAME = "testgroupx"
LOCATION = 'centralus'
NETWORK_NAME = "networknamex"
VIRTUAL_MACHINE_NAME = "virtualmachinex11"
SUBNET_NAME = "subnetx"
INTERFACE_NAME = "interfacex"
your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

RS_VAULT = 'my-vault'

def main():
    # Create resource group
    resource_group = resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})

    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': LOCATION,
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
            'location': LOCATION,
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
            "location": LOCATION,
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
    print(f"Create virtual machine:{vm}")

    # Create Recovery Services vault
    recovery_services = recovery_services_client.vaults.begin_create_or_update(
        GROUP_NAME,
        RS_VAULT,
        {
            "location": LOCATION,
            "sku": {
                "name": "standard"
            },
            "properties": {}
        }
    ).result()
    print(f"Create recovery services vault:\n{recovery_services}")


    # Configure backup parameters
    filter_string = "backupManagementType eq \'AzureIaasVM\'"
    protectable_item = recovery_services_backup_client.backup_protectable_items.list(RS_VAULT, GROUP_NAME, filter_string)
    arm_id = list(protectable_item)[0].id
    container_uri = re.search('(?<=/protectionContainers/)[^/]+', arm_id).group()
    item_uri = re.search('(?<=protectableItems/)[^/]+', arm_id).group()

    backup_props = {'protected_item_type': 'Microsoft.Compute/virtualMachines',
                    'source_resource_id': f'/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Compute/virtualMachines/{VIRTUAL_MACHINE_NAME}',
                    'policy_id': f'/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.RecoveryServices/vaults/{RS_VAULT}/backupPolicies/DefaultPolicy',
                    }

    # Azure VM enable backup
    backup = recovery_services_backup_client.protected_items.create_or_update(
        vault_name=RS_VAULT,
        resource_group_name=GROUP_NAME,
        fabric_name='Azure',
        container_name=container_uri,
        protected_item_name=item_uri,
        parameters=ProtectedItemResource(properties=backup_props)
    )

    # Start backup
    backup_now = recovery_services_backup_client.backups.trigger(
        vault_name=RS_VAULT,
        resource_group_name=GROUP_NAME,
        fabric_name='Azure',
        container_name=container_uri,
        protected_item_name=item_uri,
        parameters=BackupRequestResource(properties=BackupRequest(object_type="AzureIaaSVM"))
    )
    print('Finish')

    # clean deployment
    recovery_services_backup_client.protected_items.delete(
        vault_name=RS_VAULT,
        resource_group_name=GROUP_NAME,
        fabric_name='Azure',
        container_name=container_uri,
        protected_item_name=item_uri,
    )
    recovery_services_client.vaults.delete(resource_group_name=GROUP_NAME, vault_name=RS_VAULT)
    print('Delete RS vault')

    resource_client.resource_groups.begin_delete(resource_group_name=GROUP_NAME)
    print('Delete Resource Group')


if __name__ == '__main__':
    main()

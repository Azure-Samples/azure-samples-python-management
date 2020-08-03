import os
import random
import string

import azure.mgmt.compute as mgmt_compute
import azure.mgmt.network as mgmt_network
import azure.mgmt.resource as mgmt_resource
from azure.mgmt.compute import models as compute_models
from azure.mgmt.network import models as network_models
from azure.mgmt.resource.resources import models as resource_models
from azure.identity import DefaultAzureCredential

YOUR_PASSWORD = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(21))

class createVMSample(object):

    def __init__(self, group_name, location):
        self.location = location

        self.subscription_id = os.environ.get("SUBSCRIPTION_ID", None)

        # Use 2019-07-01 api version to test create VM
        self.compute_client = mgmt_compute.ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id,
            api_version="2019-07-01"
        )
        self.network_client = mgmt_network.NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )
        self.resource_client = mgmt_resource.ResourceManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

        self.group = self.resource_client.resource_groups.create_or_update(
            group_name,
            # model style
            resource_models.ResourceGroup(
                location=self.location
            )

            # json style
            # {'location': self.location}
        )

    def create_virtual_network(self, group_name, location, network_name, subnet_name):

        result = self.network_client.virtual_networks.begin_create_or_update(
            group_name,
            network_name,
            # model style
            network_models.VirtualNetwork(
                location=location,
                address_space=network_models.AddressSpace(
                    address_prefixes=['10.0.0.0/16']
                )
            )
            
            # json style
            # {
            #     'location': location,
            #     'address_space': {
            #         'address_prefixes': ['10.0.0.0/16']
            #     }
            # }
        )
        vnet = result.result()

        async_subnet_creation = self.network_client.subnets.begin_create_or_update(
            group_name,
            network_name,
            subnet_name,
            # model style
            network_models.Subnet(
                address_prefix='10.0.0.0/24'
            )

            # json style
            # {'address_prefix': '10.0.0.0/24'}
        )
        subnet = async_subnet_creation.result()

        return (vnet, subnet)

    def create_network_interface(self, group_name, location, nic_name, subnet):

        async_nic_creation = self.network_client.network_interfaces.begin_create_or_update(
            group_name,
            nic_name,
            # model style
            network_models.NetworkInterface(
                location=location,
                ip_configurations=[
                    network_models.NetworkInterfaceIPConfiguration(
                        name="MyIpConfig",
                        subnet=network_models.Subnet(
                            id=subnet.id
                        )
                    )
                ]
            )

            # json style
            # {
            #     'location': location,
            #     'ip_configurations': [{
            #         'name': 'MyIpConfig',
            #         'subnet': {
            #             'id': subnet.id
            #         }
            #     }]
            # }
        )
        nic = async_nic_creation.result()

        return nic

    def create_vm(self, vm_name, network_name, subnet_name, interface_name):
        group_name = self.group.name
        location = self.location

        # create network
        vnet, subnet = self.create_virtual_network(group_name, location, network_name, subnet_name)
        nic = self.create_network_interface(group_name, location, interface_name, subnet)

        # Create a vm with empty data disks.
        # model style
        model_style_vm = compute_models.VirtualMachine(
            location=location,
            hardware_profile=compute_models.HardwareProfile(
                vm_size="Standard_D2_v2"
            ),
            storage_profile=compute_models.StorageProfile(
                image_reference=compute_models.ImageReference(
                    sku="2016-Datacenter",
                    publisher="MicrosoftWindowsServer",
                    version="latest",
                    offer="WindowsServer"
                ),
                os_disk=compute_models.OSDisk(
                    caching=compute_models.CachingTypes.read_write,
                    managed_disk=compute_models.ManagedDiskParameters(
                        storage_account_type="Standard_LRS"
                    ),
                    name="myVMosdisk",
                    create_option="FromImage"
                ),
                data_disks=[
                    compute_models.DataDisk(
                        disk_size_gb=1023,
                        create_option="Empty",
                        lun=0
                    ),
                    compute_models.DataDisk(
                        disk_size_gb=1023,
                        create_option="Empty",
                        lun=1
                    )
                ]
            ),
            os_profile=compute_models.OSProfile(
                admin_username="testuser",
                computer_name="myVM",
                admin_password=YOUR_PASSWORD,
                windows_configuration=compute_models.WindowsConfiguration(
                    enable_automatic_updates=True
                )
            ),
            network_profile=compute_models.NetworkProfile(
                network_interfaces=[
                    compute_models.NetworkInterfaceReference(
                        id=nic.id,
                        primary=True
                    )
                ]
            )
        )

        # json style
        json_style_vm = {
          "location": location,
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
            "admin_password": YOUR_PASSWORD,
            "windows_configuration": {
              "enable_automatic_updates": True  # need automatic update for reimage
            }
          },
          "network_profile": {
            "network_interfaces": [
              {
                "id": nic.id,
                "primary": True
              }
            ]
          }
        }
        result = self.compute_client.virtual_machines.begin_create_or_update(
            group_name,
            vm_name,
            model_style_vm
        )
        vm = result.result()
        print("Create VM successfully\nVM:\n{}".format(vm))


def main():
    print("init sample.")
    sample = createVMSample('testvmmultiapi', 'eastus')

    print("create vm ...")
    sample.create_vm('testvm', 'testnetwork', 'testsubnet', 'testinterface')

    print("finish.")


if __name__ == '__main__':
    main()

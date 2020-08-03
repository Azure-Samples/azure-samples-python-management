import asyncio
import os
import random
import string

import azure.mgmt.compute.aio as mgmt_compute
import azure.mgmt.network.aio as mgmt_network
import azure.mgmt.resource.resources.aio as mgmt_resource
from azure.mgmt.compute import models as compute_models
from azure.mgmt.network import models as network_models
from azure.mgmt.resource.resources import models as resource_models
from azure.identity.aio import DefaultAzureCredential

YOUR_PASSWORD = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(21))

class createVMSample(object):

    def __init__(self, group_name, location):
        self.location = location
        self.group_name = group_name

        self.subscription_id = os.environ.get("SUBSCRIPTION_ID", None)

        self.credential = DefaultAzureCredential()
        self.compute_client = mgmt_compute.ComputeManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )
        self.network_client = mgmt_network.NetworkManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )
        self.resource_client = mgmt_resource.ResourceManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )

    async def init_group(self):
        print("Init Group: {}".format(self.group_name))
        self.group = await self.resource_client.resource_groups.create_or_update(
            self.group_name,
            # model style
            resource_models.ResourceGroup(
                location=self.location
            )

            # json style
            # {'location': self.location}
        )

    async def close(self):
        # Comment this delete operation, if you want to keep virtual machine
        print("Delete Group {}".format(self.group_name))
        await self.resource_client.resource_groups.delete(
            self.group_name
        )
        await self.compute_client.close()
        await self.network_client.close()
        await self.resource_client.close()
        await self.credential.close()

    async def create_virtual_network(self, group_name, location, network_name, subnet_name):

        vnet = await self.network_client.virtual_networks.create_or_update(
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

        subnet = await self.network_client.subnets.create_or_update(
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

        return (vnet, subnet)

    async def create_network_interface(self, group_name, location, nic_name, subnet):

        nic = await self.network_client.network_interfaces.create_or_update(
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

        return nic

    async def create_vm(self, vm_name, network_name, subnet_name, interface_name):
        group_name = self.group.name
        location = self.location

        # create network
        _, subnet = await self.create_virtual_network(group_name, location, network_name, subnet_name)
        nic = await self.create_network_interface(group_name, location, interface_name, subnet)

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
        vm = await self.compute_client.virtual_machines.create_or_update(
            group_name,
            vm_name,
            model_style_vm
        )
        print("Create VM successfully\nVM:\n{}".format(vm))


async def main():
    print("init sample.")
    # sample = createVMSample('testgroupvm', 'eastus')
    sample = createVMSample('testgroupvm', 'eastus')
    await sample.init_group()

    print("create vm ...")
    await sample.create_vm('testvm', 'testnetwork', 'testsubnet', 'testinterface')

    print("closing ...")
    await sample.close()

    print("finish.")


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()

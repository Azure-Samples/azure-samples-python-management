import os
import azure.mgmt.compute
import azure.mgmt.network
import azure.mgmt.resource
from azure.common.credentials import ServicePrincipalCredentials

class createVMSample(object):

    def __init__(self, group_name, location):
        self.location = location

        tenant = os.environ.get("AZURE_TENANT_ID", None)
        client_id = os.environ.get("AZURE_CLIENT_ID", None)
        secret = os.environ.get("AZURE_CLIENT_SECRET", None)
        subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
        self.subscription_id = subscription_id

        credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=secret,
            tenant=tenant
        )
        self.compute_client = azure.mgmt.compute.ComputeManagementClient(credentials=credentials, subscription_id=self.subscription_id)
        self.network_client = azure.mgmt.network.NetworkManagementClient(credentials=credentials, subscription_id=self.subscription_id)
        self.resource_client = azure.mgmt.resource.ResourceManagementClient(credentials=credentials, subscription_id=self.subscription_id)

        self.group = self.resource_client.resource_groups.create_or_update(
            group_name,
            {'location': self.location}
        )

    def create_virtual_network(self, group_name, location, network_name, subnet_name):
      
        result = self.network_client.virtual_networks.create_or_update(
            group_name,
            network_name,
            {
                'location': location,
                'address_space': {
                    'address_prefixes': ['10.0.0.0/16']
                }
            },
        )
        result_create = result.result()

        async_subnet_creation = self.network_client.subnets.create_or_update(
            group_name,
            network_name,
            subnet_name,
            {'address_prefix': '10.0.0.0/24'}
        )
        subnet_info = async_subnet_creation.result()
          
        return subnet_info

    def create_network_interface(self, group_name, location, nic_name, subnet):

        async_nic_creation = self.network_client.network_interfaces.create_or_update(
            group_name,
            nic_name,
            {
                'location': location,
                'ip_configurations': [{
                    'name': 'MyIpConfig',
                    'subnet': {
                        'id': subnet.id
                    }
                }]
            }
        )
        nic_info = async_nic_creation.result()

        return nic_info.id

    def create_vm(self, vm_name, network_name, subnet_name, interface_name):
        group_name = self.group.name
        location = self.location

        # create network
        subnet = self.create_virtual_network(group_name, location, network_name, subnet_name)
        nic_id = self.create_network_interface(group_name, location, interface_name, subnet)

        # Create a vm with empty data disks.[put]
        BODY = {
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
                "id": nic_id,
                "properties": {
                  "primary": True
                }
              }
            ]
          }
        }
        result = self.compute_client.virtual_machines.create_or_update(group_name, vm_name, BODY)
        result = result.result()


def main():
    print("init sample.")
    sample = createVMSample('testgroupvm', 'eastus')

    print("create vm ...")
    sample.create_vm('testvm', 'testnetwork', 'testsubnet', 'testinterface')

    print("finish.")


if __name__ == '__main__':
    main()

import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from haikunator import Haikunator

haikunator = Haikunator()

# Azure Datacenter
LOCATION = 'westus'

# Resource Group
GROUP_NAME = 'azure-sample-group-loadbalancer'

# Network
VNET_NAME = 'azure-sample-vnet'
SUBNET_NAME = 'azure-sample-subnet'
DOMAIN_LABEL_NAME = 'testdns'+haikunator.haikunate()
PUBLIC_IP_NAME = 'azure-sample-publicip'

# Load balancer
LB_NAME = 'azure-sample-loadbalancer'
FIP_NAME = 'azure-sample-frontendipname'
ADDRESS_POOL_NAME = 'azure-sample-addr-pool'
PROBE_NAME = 'azure-sample-probe'
LB_RULE_NAME = 'azure-sample-lb-rule'

NETRULE_NAME_1 = 'azure-sample-netrule1'
NETRULE_NAME_2 = 'azure-sample-netrule2'

FRONTEND_PORT_1 = 21
FRONTEND_PORT_2 = 23
BACKEND_PORT = 22

# VM
AVAILABILITY_SET_NAME = 'azure-sample-availabilityset'
OS_DISK_NAME = 'azure-sample-osdisk'
STORAGE_ACCOUNT_NAME = haikunator.haikunate(delimiter='')

IP_CONFIG_NAME = 'azure-sample-ip-config'
VMS_INFO = {
    1: {
        'name': 'Web1',
        'nic_name': 'azure-sample-nic1',
        'username': 'notadmin1',
        'password': 'Pa$$w0rd91'
    },
    2: {
        'name': 'Web2',
        'nic_name': 'azure-sample-nic2',
        'username': 'notadmin2',
        'password': 'Pa$$w0rd92'
    }
}

# Ubuntu config
PUBLISHER = 'Canonical'
OFFER = 'UbuntuServer'
SKU = '15.10'
VERSION = '15.10.201603150'

# Windows config
#PUBLISHER = 'microsoftwindowsserver'
#OFFER = 'windowsserver'
#SKU = '2012-r2-datacenter'

# Manage resources and resource groups - create, update and delete a resource group,
# deploy a solution into a resource group, export an ARM template. Create, read, update
# and delete a resource
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#


def run_example():
    """Resource Group management example."""
    #
    # Create all clients with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111')  # your Azure Subscription Id
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    storage_client = StorageManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)

    # Create Resource group
    print('Create Resource Group')
    resource_client.resource_groups.create_or_update(
        GROUP_NAME, {'location': LOCATION})

    # Create PublicIP
    print('Create Public IP')
    public_ip_parameters = {
        'location': LOCATION,
        'public_ip_allocation_method': 'static',
        'dns_settings': {
            'domain_name_label': DOMAIN_LABEL_NAME
        },
        'idle_timeout_in_minutes': 4
    }
    async_publicip_creation = network_client.public_ip_addresses.create_or_update(
        GROUP_NAME,
        PUBLIC_IP_NAME,
        public_ip_parameters
    )
    public_ip_info = async_publicip_creation.result()

    # Building a FrontEndIpPool
    print('Create FrontEndIpPool configuration')
    frontend_ip_configurations = [{
        'name': FIP_NAME,
        'private_ip_allocation_method': 'Dynamic',
        'public_ip_address': {
            'id': public_ip_info.id
        }
    }]

    # Building a BackEnd address pool
    print('Create BackEndAddressPool configuration')
    backend_address_pools = [{
        'name': ADDRESS_POOL_NAME
    }]

    # Building a HealthProbe
    print('Create HealthProbe configuration')
    probes = [{
        'name': PROBE_NAME,
        'protocol': 'Http',
        'port': 80,
        'interval_in_seconds': 15,
        'number_of_probes': 4,
        'request_path': 'healthprobe.aspx'
    }]

    # Building a LoadBalancer rule
    print('Create LoadBalancerRule configuration')
    load_balancing_rules = [{
        'name': LB_RULE_NAME,
        'protocol': 'tcp',
        'frontend_port': 80,
        'backend_port': 80,
        'idle_timeout_in_minutes': 4,
        'enable_floating_ip': False,
        'load_distribution': 'Default',
        'frontend_ip_configuration': {
            'id': construct_fip_id(subscription_id)
        },
        'backend_address_pool': {
            'id': construct_bap_id(subscription_id)
        },
        'probe': {
            'id': construct_probe_id(subscription_id)
        }
    }]

    # Building InboundNATRule1
    print('Create InboundNATRule1 configuration')
    inbound_nat_rules = [{
        'name': NETRULE_NAME_1,
        'protocol': 'tcp',
        'frontend_port': FRONTEND_PORT_1,
        'backend_port': BACKEND_PORT,
        'enable_floating_ip': False,
        'idle_timeout_in_minutes': 4,
        'frontend_ip_configuration': {
            'id': construct_fip_id(subscription_id)
        }
    }]

    # Building InboundNATRule2
    print('Create InboundNATRule2 configuration')
    inbound_nat_rules.append({
        'name': NETRULE_NAME_2,
        'protocol': 'tcp',
        'frontend_port': FRONTEND_PORT_2,
        'backend_port': BACKEND_PORT,
        'enable_floating_ip': False,
        'idle_timeout_in_minutes': 4,
        'frontend_ip_configuration': {
            'id': construct_fip_id(subscription_id)
        }
    })

    # Creating Load Balancer
    print('Creating Load Balancer')
    lb_async_creation = network_client.load_balancers.create_or_update(
        GROUP_NAME,
        LB_NAME,
        {
            'location': LOCATION,
            'frontend_ip_configurations': frontend_ip_configurations,
            'backend_address_pools': backend_address_pools,
            'probes': probes,
            'load_balancing_rules': load_balancing_rules,
            'inbound_nat_rules': inbound_nat_rules
        }
    )
    lb_info = lb_async_creation.result()

    ##############################################################
    # From here, we create the VM and link the LB inside the NIC #
    ##############################################################

    # Create VNet
    print('Create Vnet')
    async_vnet_creation = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        {
            'location': LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
    async_vnet_creation.wait()

    # Create Subnet
    async_subnet_creation = network_client.subnets.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )
    subnet_info = async_subnet_creation.result()

    # Creating NIC
    print('Creating NetworkInterface 1')

    back_end_address_pool_id = lb_info.backend_address_pools[0].id

    inbound_nat_rule_1_id = lb_info.inbound_nat_rules[0].id
    async_nic1_creation = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        VMS_INFO[1]['nic_name'],
        create_nic_parameters(
            subnet_info.id, back_end_address_pool_id, inbound_nat_rule_1_id)
    )

    inbound_nat_rule_2_id = lb_info.inbound_nat_rules[1].id
    print('Creating NetworkInterface 2')
    async_nic2_creation = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        VMS_INFO[2]['nic_name'],
        create_nic_parameters(
            subnet_info.id, back_end_address_pool_id, inbound_nat_rule_2_id)
    )

    nic1_info = async_nic1_creation.result()
    nic2_info = async_nic2_creation.result()

    # Create availability set
    print('Create availability set')
    availability_set_info = compute_client.availability_sets.create_or_update(
        GROUP_NAME,
        AVAILABILITY_SET_NAME,
        {'location': LOCATION}
    )

    # Create a storage account
    print('Create a storage account')
    storage_async_operation = storage_client.storage_accounts.create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            'sku': {'name': 'standard_lrs'},
            'kind': 'storage',
            'location': LOCATION
        }
    )
    storage_async_operation.wait()

    # Create VMs
    print('Creating Virtual Machine 1')
    vm_parameters1 = create_vm_parameters(
        nic1_info.id, availability_set_info.id, VMS_INFO[1])
    async_vm1_creation = compute_client.virtual_machines.create_or_update(
        GROUP_NAME, VMS_INFO[1]['name'], vm_parameters1)
    async_vm1_creation.wait()

    print('Creating Virtual Machine 2')
    vm_parameters2 = create_vm_parameters(
        nic2_info.id, availability_set_info.id, VMS_INFO[2])
    async_vm2_creation = compute_client.virtual_machines.create_or_update(
        GROUP_NAME, VMS_INFO[2]['name'], vm_parameters2)
    async_vm2_creation.wait()

    provide_vm_login_info_to_user(
        1, public_ip_info, FRONTEND_PORT_1, VMS_INFO[1])
    provide_vm_login_info_to_user(
        2, public_ip_info, FRONTEND_PORT_2, VMS_INFO[2])

    input("Press enter to delete this Resource Group.")

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))


def construct_fip_id(subscription_id):
    """Build the future FrontEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/frontendIPConfigurations/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, FIP_NAME
    )


def construct_bap_id(subscription_id):
    """Build the future BackEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/backendAddressPools/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, ADDRESS_POOL_NAME
    )


def construct_probe_id(subscription_id):
    """Build the future ProbeId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/probes/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, PROBE_NAME
    )


def provide_vm_login_info_to_user(num, public_ip_info, frontend_port, vm_info):
    """Print on the console the connection information for a given VM.
    """
    print('\n\nLogin information for the {} VM: {}'.format(
        num, vm_info['name']))
    print('-------------------------------------------')
    print('ssh to ip:port - {}:{}'.format(public_ip_info.ip_address, frontend_port))
    print('username       - {}'.format(vm_info['username']))
    print('password       - {}'.format(vm_info['password']))


def create_nic_parameters(subnet_id, address_pool_id, natrule_id):
    """Create the NIC parameters structure.
    """
    return {
        'location': LOCATION,
        'ip_configurations': [{
            'name': IP_CONFIG_NAME,
            'subnet': {
                'id': subnet_id
            },
            'load_balancer_backend_address_pools': [{
                'id': address_pool_id
            }],
            'load_balancer_inbound_nat_rules': [{
                'id': natrule_id
            }]
        }]
    }


def create_vm_parameters(nic_id, availset_id, vm_info):
    """Create the VM parameters structure.
    """
    return {
        'location': LOCATION,
        'os_profile': {
            'computer_name': vm_info['name'],
            'admin_username': vm_info['username'],
            'admin_password': vm_info['password']
        },
        'hardware_profile': {
            'vm_size': 'Standard_DS1'
        },
        'storage_profile': {
            'image_reference': {
                'publisher': PUBLISHER,
                'offer': OFFER,
                'sku': SKU,
                'version': VERSION
            },
            'os_disk': {
                'name': OS_DISK_NAME,
                'caching': 'None',
                'create_option': 'fromImage',
                'vhd': {
                    'uri': 'https://{}.blob.core.windows.net/vhds/{}.vhd'.format(
                        STORAGE_ACCOUNT_NAME, vm_info['name'])
                }
            },
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic_id,
                'primary': True
            }]
        },
        'availability_set': {
            'id': availset_id
        }
    }


if __name__ == "__main__":
    run_example()

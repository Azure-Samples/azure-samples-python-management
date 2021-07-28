import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network import models as network_models
from azure.mgmt.compute import ComputeManagementClient

# Azure Datacenter
LOCATION = 'eastus'
SKU = 'Standard'
# Resource Group
GROUP_NAME = 'myPublicLoadBalancer1'

# Network
VNET_NAME = 'myVNet'
ADDRESS_PREFIXES = '10.1.0.0/16'
SUBNET_NAME = 'myBackendSubnet'
SUBNET_PREFIXES = '10.1.0.0/24'

# Nic ip-config
NIC_IP_CONFIG_NAME = 'ipconfig1'

# Public IP address for the bastion host
BASTION_PUBLIC_IP_NAME = 'myBastionIP'

# Bastion subnet
IP_CONFIG_NAME = 'myBastionIPConfig'
BASTION_SUBNET_NAME = 'AzureBastionSubnet'
BASTION_SUBNET_PREFIXES = '10.1.1.0/24'

# Bastion host
BASTION_NAME = 'myBastionHost'

# Network security group
NSG_NAME = 'myNSG'

# Network Security Group Rule
NSG_RULE_NAME = 'myNSGRuleHTTP'

# Network interfaces for the virtual machines
NIC_NAMES = ['myNicVM1', 'myNicVM2', 'myNicVM3']

# Virtual machine
VM_NAMES = ['myVM1', 'myVM2', 'myVM3']
# VN_IMAGE = 'win2019datacenter'
VM_ADMIN_USERNAME = 'azureuser'
VM_ADMIN_PASSEORD = 'P@ssw0rd123'

# Public IP address - Standard
PUBLIC_IP_NAME = 'myPublicIP'

# Public Load balancer
LB_NAME = 'myLoadBalancer'
FIP_NAME = 'myFrontEnd'
BP_NAME = 'myBackEndPool'

# Health probe
LB_PROBE_NAME = 'myHealthProbe'
LB_PROTOCOL = 'tcp'
LB_PORT = 80

# Load balancer rule
LB_RELE_NAME = 'myHTTPRule'

# Single IP for the outbound connectivity
PUBLIC_IP_OB_NAME = 'myPublicIPOutbound'

# Public IP prefix for the outbound connectivity
PUBLIC_IP_PREDIX_OB_NAME = 'myPublicIPPrefixOutbound'
PUBLIC_IP_PREDIX_OB_LENGTH = 28

# Outbound frontend IP configuration
FIP_OB_NAME = 'myFrontEndOutbound'

# Outbound pool
OB_POOL_NAME = 'myBackendPoolOutbound'

# Oubtbound rule
OB_RULE = 'myOutboundRule'

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

def run_example():
    import time
    start_time = time.time()
    """Resource Group management example."""
    #
    # Create all clients with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111')  # your Azure Subscription Id

    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )

    # Create Resource group
    rg = resource_client.resource_groups.create_or_update(
        GROUP_NAME, {'location': LOCATION})
    print('Create Resource Group:\n{}'.format(rg))

    # Create VNet
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VNET_NAME,
        network_models.VirtualNetwork(
            location=LOCATION,
            address_space=network_models.AddressSpace(
                address_prefixes=[ADDRESS_PREFIXES]
            ),
            subnets=[network_models.Subnet(
                name=SUBNET_NAME,
                address_prefix=SUBNET_PREFIXES
            ), ]
        )
    ).result()
    print("Create Vnet:\n{}".format(network))

    # Create PublicIP for the Bastion Host
    bastion_public_ip = network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        BASTION_PUBLIC_IP_NAME,
        network_models.PublicIPAddress(
            location=LOCATION,
            public_ip_allocation_method="Static",
            sku=network_models.PublicIPPrefixSku(name="Standard")
        )
    ).result()
    print("Create Public IP for the bastion host:\n{}".format(bastion_public_ip))

    # Create Bastion Subnet
    bastion_subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VNET_NAME,
        BASTION_SUBNET_NAME,
        {'address_prefix': BASTION_SUBNET_PREFIXES}
    ).result()
    print("Create a bastion subnet:\n{}".format(bastion_subnet))

    # Create Bastion Host
    ip_configuration = network_models.BastionHostIPConfiguration(
        name=NIC_IP_CONFIG_NAME,
        subnet=network_models.SubResource(id=bastion_subnet.id),
        public_ip_address=network_models.SubResource(id=bastion_public_ip.id)
        )
    bastion_parameters = network_models.BastionHost(
        location=LOCATION,
        ip_configurations=[ip_configuration]
        )

    bastion_host = network_client.bastion_hosts.begin_create_or_update(
        GROUP_NAME,
        BASTION_NAME,
        parameters=bastion_parameters
    ).result()
    print("Create a bastion host:\n{}".format(bastion_host))

    # Create Network Security Group
    nsg_parameters = network_models.NetworkSecurityGroup(location=LOCATION)
    network_security_group = network_client.network_security_groups.begin_create_or_update(
        GROUP_NAME,
        NSG_NAME,
        parameters=nsg_parameters
    ).result()
    print("Create Network Security Group:\n{}".format(network_security_group))

    # Create Network Security Group Rule
    nsg_rule_parameters = network_models.SecurityRule(
        protocol='*',
        direction='inbound',
        source_address_prefix='*',
        source_port_range='*',
        destination_address_prefix='*',
        destination_port_range=80,
        access='allow',
        priority=200
    )
    nsg_rule = network_client.security_rules.begin_create_or_update(
        GROUP_NAME,
        NSG_NAME,
        NSG_RULE_NAME,
        nsg_rule_parameters
    ).result()
    print("Create Network Security Group Rule:\n{}".format(nsg_rule))

    # Create Backend Servers - Standard
    # Create Network Interfaces for the VMs
    network_interface_parameters = network_models.NetworkInterface(
        location=LOCATION,
        enable_accelerated_networking=True,
        ip_configurations=[network_models.NetworkInterfaceIPConfiguration(
            name=NIC_IP_CONFIG_NAME,
            subnet=network_models.Subnet(id=network.subnets[0].id)
        ),
        ],
        network_security_group=network_models.NetworkSecurityGroup(id=network_security_group.id)
    )
    network_interfaces = []
    for nic_name in NIC_NAMES:
        network_interface = network_client.network_interfaces.begin_create_or_update(
            GROUP_NAME,
            nic_name,
            network_interface_parameters
        ).result()
        network_interfaces.append(network_interface)
        print("Create Network Interface named {}:\n{}".format(nic_name, network_interface))

    ##############################################################
    # From here, we create the VM and link the LB inside the NIC #
    ##############################################################

    # Create VMs
    vms = []
    for i in range(3):
        vm = compute_client.virtual_machines.begin_create_or_update(
            GROUP_NAME,
            VM_NAMES[i],
            {
                "location": LOCATION,
                "hardware_profile": {
                    "vm_size": "Standard_D2_v2"
                },
                "storage_profile": {
                    "image_reference": {
                        "sku": "2019-Datacenter",
                        "publisher": "MicrosoftWindowsServer",
                        "version": "latest",
                        "offer": "WindowsServer"
                    },
                    "os_disk": {
                        "caching": "ReadWrite",
                        "managed_disk": {
                            "storage_account_type": "Standard_LRS"
                        },
                        "name": "myVMosdisk"+str(i+1),
                        "create_option": "FromImage"
                    },
                    "data_disks": [
                        {
                            "disk_size_gb": "1023",
                            "create_option": "Empty",
                            "lun": "0"
                        }
                    ]
                },
                "os_profile": {
                    "admin_username": VM_ADMIN_USERNAME,
                    "computer_name": "myVM",
                    "admin_password": VM_ADMIN_PASSEORD,
                    "windows_configuration": {
                        "enable_automatic_updates": True  # need automatic update for reimage
                    }
                },
                "network_profile": {
                    "network_interfaces": [
                        {
                            "id": network_interfaces[i].id,
                            "properties": {
                                "primary": True
                            }
                        }
                    ]
                }
            }
        ).result()
        vms.append(vm)
        print('Create VM{} :\n{}'.format(str(i+1), vm))

    # Create PublicIP for the Load Balancer
    public_ip = network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_NAME,
        network_models.PublicIPAddress(
            location=LOCATION,
            public_ip_allocation_method="Static",
            sku=network_models.PublicIPPrefixSku(name="Standard")
        )
    ).result()
    print("Create PublicIP for the Load Balancer:\n{}".format(public_ip))

    # Create Load Balancer
    load_balancer_parameters = network_models.LoadBalancer(
        location=LOCATION,
        sku=network_models.Sku(name=SKU),
        frontend_ip_configurations=[
            network_models.FrontendIPConfiguration(
                name=FIP_NAME,
                public_ip_address=network_models.PublicIPAddress(
                    id=public_ip.id
                )
            )
        ],
        backend_address_pools=[
            network_models.BackendAddressPool(
                name=BP_NAME
            )
        ]
    )

    load_balancer = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result()
    print("Create Load Balancer:\n{}".format(load_balancer))

    # Create Health Probe
    load_balancer_parameters.probes = [
        network_models.Probe(
            protocol=LB_PROTOCOL,
            port=LB_PORT,
            name=LB_PROBE_NAME
        )
    ]
    lb_probe = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result().probes
    print("Create Health Probe: \n{}".format(eval(str(lb_probe[0]))))

    # Create Load Balancer Rule
    load_balancer_parameters.load_balancing_rules = [
        network_models.LoadBalancingRule(
            name=LB_RELE_NAME,
            protocol='tcp',
            frontend_port=80,
            backend_port=80,
            frontend_ip_configuration=network_models.SubResource(id=load_balancer.frontend_ip_configurations[0].id),
            backend_address_pool=network_models.SubResource(id=load_balancer.backend_address_pools[0].id),
            probe=network_models.SubResource(id=lb_probe[0].id),
            disable_outbound_snat=True,
            idle_timeout_in_minutes=15,
            enable_floating_ip=True
        )
    ]
    lb_rule = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result().load_balancing_rules
    print("Create Load Balancer Rule: \n{}".format(lb_rule[0]))

    # Add VMs to Load Balancer Backend Pool
    for i in range(3):
        for nic_ipconf in network_interfaces[i].ip_configurations:
            if nic_ipconf.name == NIC_IP_CONFIG_NAME:
                nic_ipconf.load_balancer_backend_address_pools = [load_balancer.backend_address_pools[0],
                                                                  ]
        add_vm_to_lb_bp = network_client.network_interfaces.begin_create_or_update(
            GROUP_NAME,
            NIC_NAMES[i],
            network_interfaces[i]
        ).result().ip_configurations
        print("Add {} to Load Balancer Backend Pool: \n{}".format(NIC_NAMES[i], add_vm_to_lb_bp))

    # Create Public IP for the Outbound Connectivity
    outbound_rule_ip = network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_OB_NAME,
        network_models.PublicIPAddress(
            location=LOCATION,
            public_ip_allocation_method="Static",
            sku=network_models.PublicIPPrefixSku(name="Standard")
        )
    ).result()
    print("Create Public IP for the Outbound Connectivity:\n{}".format(outbound_rule_ip))

    # Create Frontend IP Configuration
    load_balancer_parameters.frontend_ip_configurations.append(
        network_models.FrontendIPConfiguration(
            name=FIP_OB_NAME,
            public_ip_address=outbound_rule_ip
        )
    )
    lb_fip_config = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result().frontend_ip_configurations
    print("Create Frontend IP Configuration:\n{}".format(lb_fip_config[-1]))

    # Create Outbound Pool
    load_balancer_parameters.backend_address_pools.append(
        network_models.BackendAddressPool(
            name=OB_POOL_NAME,
        )
    )
    lb_ob_pool = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result().backend_address_pools
    print("Create Outbound Pool:\n{}".format(lb_ob_pool[-1]))

    # Create Outbound Rule for the Outbound Backend Pool
    load_balancer_parameters.outbound_rules = [
        network_models.OutboundRule(
            name=OB_RULE,
            frontend_ip_configurations=[network_models.SubResource(id=lb_fip_config[-1].id)],
            protocol='All',
            idle_timeout_in_minutes=15,
            allocated_outbound_ports=10000,
            backend_address_pool=network_models.SubResource(id=lb_ob_pool[-1].id)
        )
    ]
    lb_ob_rule = network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LB_NAME,
        load_balancer_parameters
    ).result().outbound_rules
    print("Create Outbound Rule for the Outbound Backend Pool:\n{}".format(lb_ob_rule[-1]))

    # Add VMs to the Outbound Pool
    ob_pool_info = network_client.load_balancer_backend_address_pools.get(
        GROUP_NAME,
        LB_NAME,
        OB_POOL_NAME
    )
    for i in range(3):
        vmnic_info = network_client.network_interfaces.get(
            GROUP_NAME, NIC_NAMES[i]
        )
        for ip_conf in vmnic_info.ip_configurations:
            if ip_conf.name == NIC_IP_CONFIG_NAME:
                ip_conf.load_balancer_backend_address_pools.append(ob_pool_info)

        add_vm_to_lb_op = network_client.network_interfaces.begin_create_or_update(
            GROUP_NAME,
            NIC_NAMES[i],
            vmnic_info
        ).result().ip_configurations
        print("Add {} to Load Balancer Outbound Pool: \n{}".format(NIC_NAMES[i], add_vm_to_lb_op))

    # Get the Public IP Address of the Load Balancer
    network_public_ip_info = network_client.public_ip_addresses.get(
        GROUP_NAME, PUBLIC_IP_NAME
    )
    print("Public IP Address:\n{}".format(network_public_ip_info.ip_address))
    print("Running time: {}".format(time.time()-start_time))

    # Delete Resource group and everything in it
    input("Press enter to delete this Resource Group.")
    print('Delete Resource Group')
    delete_group = resource_client.resource_groups.begin_delete(GROUP_NAME)
    print("\nDeleted: {}".format(GROUP_NAME))


if __name__ == "__main__":
    run_example()

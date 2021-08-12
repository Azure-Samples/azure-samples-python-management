---
page_type: sample
languages:
- python
products:
- azure
description: "This sample shows how to manage a load balancer using the Azure Resource Manager APIs for Python."
urlFragment: network-python-manage-loadbalancer
---

# Getting Started with Azure Resource Manager for load balancers in Python

An Azure load balancer is a Layer-4 (TCP, UDP) type load balancer that distributes incoming traffic among healthy service instances in cloud services or virtual machines defined in a load balancer set. You can use a load balancer to provide high availability for your workloads in Azure. 

For a detailed overview of Azure load balancers, see [Azure Load Balancer overview](https://azure.microsoft.com/documentation/articles/load-balancer-overview/).

![alt tag](./load-balancer.svg)

Attached to this doc are samples that show how to manage both a pulic load balancer with outbound rules and an internal load balancer using the Azure Resource Manager APIs for Python. The samples deploy their respective load balancer then creates and deploys three Azure virtual machines behind the load balancer.

To deploy a public load balancer with outbound rules, you'll need to create and configure the following objects.

- Front end IP configuration - contains public IP addresses for incoming network traffic. 
- Back end address pool - contains network interfaces (NICs) for the virtual machines to receive network traffic from the load balancer. 
- Load balancing rules - contains rules mapping a public port on the load balancer to port in the back end address pool.
- Inbound NAT rules - contains rules mapping a public port on the load balancer to a port for a specific virtual machine in the back end address pool.
- Probes - contains health probes used to check availability of virtual machines instances in the back end address pool.
- Outbound rules - contains public IP address for outbound network traffic. 

To deploy an internal load balancer, you'll need to create and configure the following objects.

- Back end address pool - contains network interfaces (NICs) for the virtual machines to receive network traffic from the load balancer. 
- Load balancing rules - contains rules mapping a public port on the load balancer to port in the back end address pool.
- Inbound NAT rules - contains rules mapping a public port on the load balancer to a port for a specific virtual machine in the back end address pool.
- Probes - contains health probes used to check availability of virtual machines instances in the back end address pool.

You can get more information about load balancer components with Azure resource manager at [Azure Resource Manager support for Load Balancer](https://azure.microsoft.com/documentation/articles/load-balancer-arm/).

## Tasks performed in these samples

### Public load balancer with outbound rules

The sample performs the following tasks to create the load balancer and the load-balanced virtual machines: 

1. Create Resource group
2. Create VNet
3. Create PublicIP for the Bastion Host
4. Create Bastion Subnet
5. Create Bastion Host
6. Create Network Security Group
7. Create Network Security Group Rule
8. Create Backend Servers - Standard
9. Create Network Interfaces for the VMs
10. Create VMs
11. Create PublicIP for the Load Balacer
12. Create Load Balancer
13. Create Health Probe
14. Create Load Balancer Rule
15. Add VMs to Load Balancer Backend Pool
16. Create PublicIP for the Outbound Connectivity
17. Create Frontend IP Configuration
18. Create Outbound Pool
19. Create Oubound Rule for the Outbound Backend Pool
20. Add VMs to the Outbound Pool
21. Get the PublicIP Address of the Load Balancer
22. Delete Resource group and everything in it

### Internal load balancer

The sample performs the following tasks to create the load balancer and the load-balanced virtual machines: 

1. Create Resource group
2. Create VNet
3. Create PublicIP for the Bastion Host
4. Create Bastion Subnet
5. Create Bastion Host
6. Create Network Security Group
7. Create Network Security Group Rule
8. Create Backend Servers - Standard
9. Create Network Interfaces for the VMs
10. Create VMs
11. Create Load Balancer
12. Create Health Probe
13. Create Load Balancer Rule
14. Add VMs to Load Balancer Backend Pool
15. Create NIC for VM to test
16. Create VM for test
17. Delete Resource group and everything in it

## Run this sample

1. If you don't already have a Microsoft Azure subscription, you can register for a [free trial account](http://go.microsoft.com/fwlink/?LinkId=330212).

1. Install [Python](https://www.python.org/downloads/) if you haven't already.

2. We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtual environment this way:

	    pip install virtualenv
	    virtualenv mytestenv
	    cd mytestenv
	    source bin/activate

3. Clone the sample repository.
    
	    git clone https://github.com/Azure-Samples/network-python-manage-loadbalancer.git    

4. Install the dependencies using pip.

	    cd network-python-manage-loadbalancer
	    pip install -r requirements.txt    

5. Create an Azure service principal, using 
[Azure CLI](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [Azure Portal](http://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

6. Export these environment variables into your current shell. 
    
	    export AZURE_TENANT_ID={your tenant ID}
	    export AZURE_CLIENT_ID={your client ID}
	    export AZURE_CLIENT_SECRET={your client secret}
	    export AZURE_SUBSCRIPTION_ID={your subscription ID}
    
7. Run the sample for public load balancer.
    
	    python example_public_load_balancer.py
   Or
   
   Run the sample for internal load balancer.
            
	    python example_internal_load_balancer.py
   
## More information

- [Azure SDK for Python](http://github.com/Azure/azure-sdk-for-python) 

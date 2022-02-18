import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network.models import VirtualNetworkGateway, VirtualNetworkGatewayIPConfiguration, SubResource, \
    VirtualNetworkGatewaySku, VpnClientConfiguration, AddressSpace, VpnClientRootCertificate


def main():

    credentials = DefaultAzureCredential()
    subscription = os.getenv('SUBSCRIPTION_ID')

    resource_client = ResourceManagementClient(
        credential=credentials,
        subscription_id=subscription
    )
    nmclient = NetworkManagementClient(credentials, subscription)

    GROUP_NAME = 'testgroupx'  # Resource groups name
    VIRTUAL_NETWORK_NAME = 'virtualnetworkxx'
    NEW_VIRTUAL_NETWORK_GATEWAY= 'newgateway'
    SUBNET = 'GatewaySubnet'  # Must be `GatewaySubnet`
    PUBLIC_IP_ADDRESS_NAME = 'publicipaddressxxxx'
    IP_CONFIGURATION_NAME = 'default'
    root_cert = "xxxxxxx"  # root certification

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "westus"}
    )

    # - init depended resources -
    nmclient.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS_NAME,
        {
            'location': "eastus",
            'public_ip_allocation_method': 'Dynamic',
            'idle_timeout_in_minutes': 4
        }
    )

    nmclient.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
            "address_space": {
                "address_prefixes": [
                    "10.0.0.0/16"
                ]
            },
            "location": "eastus"
        }
    ).result()

    # Create subnet
    nmclient.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET,
        {
            "address_prefix": "10.0.0.0/24"
        }
    ).result()

    vn_para = VirtualNetworkGateway(
        ip_configurations=[VirtualNetworkGatewayIPConfiguration(
            private_ip_allocation_method="Dynamic",
            subnet=SubResource(
                id="/subscriptions/" + subscription + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET + ""),
            public_ip_address=SubResource(
                id="/subscriptions/" + subscription + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME + ""),
            name=IP_CONFIGURATION_NAME
        )],
        gateway_type="Vpn",
        vpn_type="RouteBased",
        enable_bgp=False,
        active=False,
        enable_dns_forwarding=False,
        sku=VirtualNetworkGatewaySku(name="VpnGw2", tier="VpnGw2"),
        vpn_client_configuration=VpnClientConfiguration(
            vpn_client_address_pool=AddressSpace(address_prefixes=["192.168.0.0/24"]),
            vpn_authentication_types=['Certificate'],
            vpn_client_root_certificates=[VpnClientRootCertificate(name="testCA", public_cert_data=root_cert)],
            vpn_client_protocols=["OpenVPN"],
        ),
        vpn_gateway_generation="Generation2",
        location="westus"
    )

    # Create virtual network gateway
    virtual_network_gateway = nmclient.virtual_network_gateways.begin_create_or_update(
        GROUP_NAME,
        NEW_VIRTUAL_NETWORK_GATEWAY,
        vn_para
    ).result()
    print(virtual_network_gateway)


if __name__ == '__main__':
    main()

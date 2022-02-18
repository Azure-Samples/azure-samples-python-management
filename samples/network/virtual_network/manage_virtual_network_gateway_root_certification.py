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

    GROUP_NAME = 'testgroup1'  # Resource groups name
    VIRTUAL_NETWORK_NAME = 'virtualnetworkx1'
    NEW_VIRTUAL_NETWORK_GATEWAY= 'newgateway1'
    SUBNET = 'GatewaySubnet'  # Must be `GatewaySubnet`
    PUBLIC_IP_ADDRESS_NAME = 'publicipaddressxxx1'
    IP_CONFIGURATION_NAME = 'default'
    LOCATION = 'westus'
    root_cert = '''MIIC5zCCAc+gAwIBAgIQTSvj+DXI4ZRDHGoSpD6iwTANBgkqhkiG9w0BAQsFADAW
MRQwEgYDVQQDDAtQMlNSb290Q2VydDAeFw0yMjAyMTYwODQ1NTNaFw0yMzAyMTYw
OTA1NTNaMBYxFDASBgNVBAMMC1AyU1Jvb3RDZXJ0MIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEA17o3fyrT0+ioAXuchiR5JLa+vTQnMNzhAYngB5nen+sq
s7eIQ64a6HSCRTHRV+KvxdF+PXgq1z/tNxbzv60bJ2x40jUAPSQROV5v5WQnJ2Yj
G/3DhiGdCho6+xyQP1yqdg+FWI5Z4R2TMz24xw3w5QJ3+9xljL9x3y2JXKb9QHKa
VwwZGgX5BYepkJIq7m9PRl0YwHfQ83/nm1RHMfwtgXVtHdvsURSKK6xvezAV40FF
iKyO22wef4AHqmddFyJm/xiWUdU3KPYjujAH1QmjBVgamTIcpOGiNr4+9+I0hWFe
hf3O6wEVll4jcmErwOD/mwZ8EIN3l49dVeBDt6wNcQIDAQABozEwLzAOBgNVHQ8B
Af8EBAMCAgQwHQYDVR0OBBYEFKBW9GjSks02EY8R47LHyfbHIC1/MA0GCSqGSIb3
DQEBCwUAA4IBAQAar4bMcpVYV457vpeYNSiymUcqEs+eFJ8kpf41Riv0xsbUOJvI
vQmgfeYQQfJnJy2QR42prQkxDxmA1sA9OZ/imFP5w9KtWWcRdqOqOYIQLimSVD/0
WMJKG/52pe0ThWHQFBfzwem1x1hn4FTKaWoweZdfGmUJDxPWWWXdBXuHJK6YVfid
LRuLIW4JAmsFW4BngnA5xsylqwYt/OZs5QoonZnWiJndBSzRQOTaF6Elk9YsaTRt
iTQRaf3NJY8n8Gfiv6qAIFySslc0UNbM1UCbJli3W8TryvLyKceOoCmkXqk7wpVj
fTXj3iNf24BhY4sF/UtDVyWxKSWtbgPSr8Qs'''  # root certification

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": LOCATION}
    )

    # - init depended resources -
    nmclient.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS_NAME,
        {
            'location': LOCATION,
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
            "location": LOCATION
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
        location=LOCATION
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

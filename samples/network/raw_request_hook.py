import json
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetworkGateway, VirtualNetworkGatewayIPConfiguration, SubResource, \
    VirtualNetworkGatewaySku, VpnClientConfiguration, AddressSpace, VpnClientRootCertificate


def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('SUBSCRIPTION_ID')

    def callback(request):
        origin_req = json.loads(request.http_request.body)
        with open('result.json', 'w') as file:
            file.write(json.dumps(origin_req, indent=4))

    nmclient = NetworkManagementClient(credentials, subscription)

    GROUP_NAME = 'testgroupx'  # Resource groups name
    VIRTUAL_NETWORK_NAME = 'virtualnetworkxx'
    NEW_VIRTUAL_NETWORK_GATEWAY = 'newgateway'
    SUBNET = 'GatewaySubnet'  # Must be `GatewaySubnet`
    PUBLIC_IP_ADDRESS_NAME = 'publicipaddressxxxx'
    IP_CONFIGURATION_NAME = 'default'
    root_cert = "xxxxxxx"  # root certification

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

    virtual_network_gateway = nmclient.virtual_network_gateways.begin_create_or_update(
        GROUP_NAME,
        NEW_VIRTUAL_NETWORK_GATEWAY,
        vn_para,
        raw_request_hook=callback
    ).result()


if __name__ == '__main__':
    main()

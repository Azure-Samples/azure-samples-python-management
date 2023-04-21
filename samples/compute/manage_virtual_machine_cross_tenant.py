# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.identity import ClientSecretCredential
from azure.mgmt.core.policies import AuxiliaryAuthenticationPolicy
from azure.mgmt.compute import ComputeManagementClient


# this docs show how to use Python SDK to authenticate across tenants. For more info, please refer to
# https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/authenticate-multi-tenant
def main():
    cred1 = ClientSecretCredential(tenant_id="your_teanantId1", client_id="your_clientId1",
                                   client_secret="your_clientSecret1")
    cred2 = ClientSecretCredential(tenant_id="your_teanantId2", client_id="your_clientId2",
                                   client_secret="your_clientSecret2")
    auth_policy = AuxiliaryAuthenticationPolicy(auxiliary_credentials=[cred1, cred2],
                                                scopes=['https://management.azure.com/.default'])
    compute_client = ComputeManagementClient(
        credential=cred1,
        subscription_id="your_subId",
        authentication_policy=auth_policy
    )

    # Create virtual machine
    vm = compute_client.virtual_machines.begin_create_or_update(...).result()
    print("Create virtual machine:\n{}".format(vm.serialize()))


if __name__ == "__main__":
    main()

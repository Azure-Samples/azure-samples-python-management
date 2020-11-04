# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    marketplaceordering_client = MarketplaceOrderingAgreements(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Get marketplace agreement
    marketplace_agreement = marketplaceordering_client.marketplace_agreements.get(
        offer_type="virtualmachine",
        publisher_id="intel-bigdl",
        offer_id="bigdl_vm",
        plan_id="bigdl_vm_0p4"
    )
    print("Get marketplace agreement:\n{}".format(marketplace_agreement))


if __name__ == "__main__":
    main()

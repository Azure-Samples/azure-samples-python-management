# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import json

# Use `from azure.identity import AzureCliCredential` if authenticating via Azure CLI for test
from azure.identity import DefaultAzureCredential

from azure.mgmt.testbase import TestBase
from azure.mgmt.testbase.models import TestBaseAccountResource
from azure.mgmt.testbase.models import TestBaseAccountSKU

def _format_json(content):
    return json.dumps(content.serialize(keep_readonly=True), indent=4, separators=(',', ': '))

def main():
    # Requesting token from Azure
    print("Requesting token from Azure...")
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    #     Use `credential = AzureCliCredential()` if authenticating via Azure CLI for test
    credential = DefaultAzureCredential()

    # Run `export SUBSCRIPTION_ID="<subscription-id>"` on Linux-based OS
    # Run `set SUBSCRIPTION_ID=<subscription-id>` on Windows
    subscription_id = os.environ.get("SUBSCRIPTION_ID", None)

    # Set variables
    resource_group = "<resource-group-name>"
    testBaseAccount_name = "contoso-testbaseAccount"
    testBaseAccount_location = "global"
    sku_name = "S0"
    sku_tier = "Standard"
    sku_locations = {"global"}

    # Create client
    testBase_client = TestBase(credential, subscription_id)

    # Create sku for TestBaseAccount
    sku = TestBaseAccountSKU(name=sku_name, tier=sku_tier, locations=sku_locations)

    # Create TestBaseAccount
    print("Creating TestBaseAccount...")
    parameters = TestBaseAccountResource(location=testBaseAccount_location, sku=sku)
    testBaseAccount = testBase_client.test_base_accounts.begin_create(resource_group, testBaseAccount_name, parameters).result()

    # Get TestBaseAccount
    print("Getting TestBaseAccount...")
    result = testBase_client.test_base_accounts.get(resource_group, testBaseAccount_name)
    print(_format_json(result))

if __name__ == "__main__":
    main()

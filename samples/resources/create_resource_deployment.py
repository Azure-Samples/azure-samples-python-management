# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient


template = {
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "location": {
        "type": "string",
        "allowedValues": [
            "East US",
            "West US",
            "West Europe",
            "East Asia",
            "South East Asia"
        ],
        "metadata": {
            "description": "Location to deploy to"
        }
        }
    },
    "resources": [
        {
        "type": "Microsoft.Compute/availabilitySets",
        "name": "availabilitySet1",
        "apiVersion": "2019-07-01",
        "location": "[parameters('location')]",
        "properties": {}
        }
    ],
    "outputs": {
        "myparameter": {
        "type": "object",
        "value": "[reference('Microsoft.Compute/availabilitySets/availabilitySet1')]"
        }
    }
}

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    DEPLOYMENT_NAME = "deploymentx"

    # Create client
    resource_client = ResourceManagementClient(
        credential=EnvironmentCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Check deployment existence
    exist_result =  resource_client.deployments.check_existence(
        GROUP_NAME,
        DEPLOYMENT_NAME
    )
    print("Check deployment existence:\n{}".format(exist_result))

    # Create deployment
    deployment = resource_client.deployments.begin_create_or_update(
        GROUP_NAME,
        DEPLOYMENT_NAME,
        {
            "properties":{
                "mode": "Incremental",
                "template": template,
                "parameters": {"location": { "value": "West US"}}
            }
        }
    ).result()
    print("Create deployment:\n{}".format(deployment))

    # Get deployment
    deployment = resource_client.deployments.get(
        GROUP_NAME,
        DEPLOYMENT_NAME
    )
    print("Get deployment:\n{}".format(deployment))

    # Validate deployment
    validation = resource_client.deployments.begin_validate(
        GROUP_NAME,
        DEPLOYMENT_NAME,
        {
            "properties": {
                "mode": "Incremental",
                "template": template,
                "parameters": {"location": { "value": "West US"}}
            }
        }
    ).result()
    print("Vlidate deployment:\n{}".format(validation))

    # Delete deployment
    resource_client.deployments.begin_delete(
        GROUP_NAME,
        DEPLOYMENT_NAME
    ).result()
    print("Delete deployment.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

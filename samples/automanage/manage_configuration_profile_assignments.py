import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.automanage import AutomanageClient


def main():
    rg = "resourceGroupName"
    profile_name = "configurationProfileName"
    vm = "vmName"
    SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')

    # Create Automanage Client
    credential = DefaultAzureCredential()
    client = AutomanageClient(credential, SUBSCRIPTION_ID)

    # Create Azure Best Practices assignment
    best_practices_assignment = {
        "properties": {
            "configurationProfile": "/providers/Microsoft.Automanage/bestPractices/AzureBestPracticesProduction",
        }
    }

    client.configuration_profile_assignments.create_or_update(
        "default", rg, vm, custom_profile_assignment)

    # Create custom profile assignment
    custom_profile_assignment = {
        "properties": {
            "configurationProfile": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{rg}/providers/Microsoft.Automanage/configurationProfiles/{profile_name}"
        }
    }

    client.configuration_profile_assignments.create_or_update(
        "default", rg, vm, best_practices_assignment)

    # Get configuration profile assignment
    assignment = client.configuration_profile_assignments.get(
        rg, "default", vm)
    print(assignment)


if __name__ == '__main__':
    main()

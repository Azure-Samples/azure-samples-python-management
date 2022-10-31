import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.security import SecurityCenter
from azure.mgmt.security.models import AdvancedThreatProtectionSetting


def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('SUBSCRIPTION_ID')

    security_client = SecurityCenter(credentials, subscription)

    # Creates or updates the Advanced Threat Protection settings on a specified resource.
    security_client.advanced_threat_protection.create(
        resource_id='<resource_id>',  # Specify resource id, e.g. "subscriptions/20ff7fc3-e762-44dd-bd96-b71116dcdc23/resourceGroups/SampleRG/providers/Microsoft.Storage/storageAccounts/samplestorageaccount"
        advanced_threat_protection_setting=AdvancedThreatProtectionSetting(is_enabled=True)
    ).result()

    # Gets the Advanced Threat Protection settings for the specified resource.
    security_features = security_client.advanced_threat_protection.get(
        resource_id='<resource_id>'  # Specify resource id
    )
    print(security_features.is_enabled)
    print(security_features.type)
    print(security_features.id)


if __name__ == '__main__':
    main()

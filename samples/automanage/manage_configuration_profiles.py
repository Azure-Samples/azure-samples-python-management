import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.automanage import AutomanageClient


def main():
    rg = "resourceGroupName"
    profile_name = "configurationProfileName"
    SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')

    # Create Automanage Client
    credential = DefaultAzureCredential()
    client = AutomanageClient(credential, SUBSCRIPTION_ID)

    # Fetch configuration profile
    profile = client.configuration_profiles.get(profile_name, rg)
    print(profile)

    # Fetch all configuration profiles in resource group
    profiles = client.configuration_profiles.list_by_resource_group(rg)
    for profile in profiles:
        print(profile)

    # Fetch all configuration profiles in resource subscription
    profiles = client.configuration_profiles.list_by_subscription()
    for profile in profiles:
        print(profile)

    # Create configuration profile
    new_profile = {
        "location": "eastus",
        "tags": {"environment": "dev"},
        "properties": {
            "configuration": {
                "Antimalware/Enable": True,
                "Antimalware/Exclusions/Paths": "",
                "Antimalware/Exclusions/Extensions": "",
                "Antimalware/Exclusions/Processes": "",
                "Antimalware/EnableRealTimeProtection": True,
                "Antimalware/RunScheduledScan": True,
                "Antimalware/ScanType": "Quick",
                "Antimalware/ScanDay": 7,
                "Antimalware/ScanTimeInMinutes": 120,
                "Backup/Enable": True,
                "Backup/PolicyName": "dailyBackupPolicy",
                "Backup/TimeZone": "UTC",
                "Backup/InstantRpRetentionRangeInDays": 2,
                "Backup/SchedulePolicy/ScheduleRunFrequency": "Daily",
                "Backup/SchedulePolicy/ScheduleRunTimes": [
                    "2022-07-21T12: 00: 00Z"
                ],
                "Backup/SchedulePolicy/SchedulePolicyType": "SimpleSchedulePolicy",
                "Backup/RetentionPolicy/RetentionPolicyType": "LongTermRetentionPolicy",
                "Backup/RetentionPolicy/DailySchedule/RetentionTimes": [
                    "2022-07-21T12: 00: 00Z"
                ],
                "Backup/RetentionPolicy/DailySchedule/RetentionDuration/Count": 180,
                "Backup/RetentionPolicy/DailySchedule/RetentionDuration/DurationType": "Days",
                "WindowsAdminCenter/Enable": False,
                "VMInsights/Enable": True,
                "AzureSecurityCenter/Enable": True,
                "UpdateManagement/Enable": True,
                "ChangeTrackingAndInventory/Enable": True,
                "GuestConfiguration/Enable": True,
                "AutomationAccount/Enable": True,
                "LogAnalytics/Enable": True,
                "BootDiagnostics/Enable": True
            }
        }
    }

    client.configuration_profiles.create_or_update(
        profile_name, rg, new_profile)

    # Delete configuration profile
    client.configuration_profiles.delete(rg, profile_name)


if __name__ == '__main__':
    main()

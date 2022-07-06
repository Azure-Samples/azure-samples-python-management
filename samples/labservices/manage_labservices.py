# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from datetime import timedelta
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.labservices import LabServicesClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -
#

def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.','')
    GROUP_NAME = "python_rg" + TIME
    LABPLAN = "python_labplan" + TIME
    LAB = "python_lab" + TIME
    LOCATION = 'southcentralus'    

    # Create clients
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    
    labservices_client = LabServicesClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": LOCATION}
    )

    # - init depended resources -
    # - end -

    # Create lab services lab plan
    LABPLANBODY = {
        "location" : LOCATION,
        "properties" : {
            "defaultConnectionProfile" : {
                "webSshAccess" : "None",
                "webRdpAccess" : "None",
                "clientSshAccess" : "None",
                "clientRdpAccess" : "Public"
            },
            "defaultAutoShutdownProfile" : {
                "shutdownOnDisconnect" : "Disabled",
                "shutdownWhenNotConnected" : "Disabled",
                "shutdownOnIdle" : "None"
            },
            "allowedRegions" : [LOCATION],
            "supportInfo" : {
                "email" : "test@test.com",
                "phone" : "123-123-1234",
                "instructions" : "test"
            }
        }
    }

    #Create Lab Plan
    poller = labservices_client.lab_plans.begin_create_or_update(
        GROUP_NAME,
        LABPLAN,
        LABPLANBODY
    )

    labplan_result = poller.result()
    print(f"Created Lab Plan: {labplan_result.name}")

    # Get LabServices Lab Plans by resource group
    labservices_client.lab_plans.list_by_resource_group(
        GROUP_NAME
    )

    #Get single LabServices Lab Plan
    labservices_labplan = labservices_client.lab_plans.get(GROUP_NAME, LABPLAN)

    print("Get lab plans")
    print(labservices_labplan)

    USAGEQUOTA = timedelta(hours=10)

    # Create LabServices Lab
    LABBODY = {
        "name": LAB,
        "location" : LOCATION,
        "properties" : {
            "networkProfile": {},
            "connectionProfile" : {
                "webSshAccess" : "None",
                "webRdpAccess" : "None",
                "clientSshAccess" : "None",
                "clientRdpAccess" : "Public"
            },
            "AutoShutdownProfile" : {
                "shutdownOnDisconnect" : "Disabled",
                "shutdownWhenNotConnected" : "Disabled",
                "shutdownOnIdle" : "None"
            },
            "virtualMachineProfile" : {
                "createOption" : "TemplateVM",
                "imageReference" : {
                    "offer": "windows-11",
                    "publisher": "microsoftwindowsdesktop",
                    "sku": "win11-21h2-pro",
                    "version": "latest"
                },
                "sku" : {
                    "name" : "Classic_Fsv2_2_4GB_128_S_SSD",
                    "capacity" : 2
                },
                "additionalCapabilities" : {
                    "installGpuDrivers" : "Disabled"
                },
                "usageQuota" : USAGEQUOTA,
                "UseSharedPassword" : "Enabled",
                "adminUser" : {
                    "username" : "testuser",
                    "password" : "JunkPwd2BeReplaced!"
                }
            },
            "securityProfile" : {
                "openAccess" : "Disabled"
            },
            "rosterProfile" : {},
            "labPlanId" : labservices_labplan.id,
            "title" : "lab-python",
            "description" : "lab 99 description updated"
        }
    }

    poller = labservices_client.labs.begin_create_or_update(
        GROUP_NAME,
        LAB,
        LABBODY
    )

    lab_result = poller.result()
    print(f"Created Lab  {lab_result.name}")

    # Get LabServices Labs
    labservices_lab = labservices_client.labs.get(GROUP_NAME,LAB)
    print("Get lab:\n{}".format(labservices_lab))
    

    # Delete Lab
    labservices_client.labs.begin_delete(
        GROUP_NAME,
        LAB
    ).result()
    print("Deleted lab.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
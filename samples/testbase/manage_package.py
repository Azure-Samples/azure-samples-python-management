# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time

# Use `from azure.identity import AzureCliCredential` if authenticating via Azure CLI for test
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient

from azure.mgmt.testbase import TestBase
from azure.mgmt.testbase.models import PackageResource
from azure.mgmt.testbase.models import TargetOSInfo
from azure.mgmt.testbase.models import Test
from azure.mgmt.testbase.models import Command
from azure.mgmt.testbase.models import GetFileUploadURLParameters
from testbase_util import format_json


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
    resource_group = "<resource-group-name>" # replace with real resource group name
    testbase_account_name = "<testbaseaccount-name>" # replace with real test base account name
    package_file_path = "<path-of-package-zip-file>" # replace with real path of the package zip file, please refer to https://aka.ms/usl-package-outline for package structure

    # Create client
    testbase_client = TestBase(credential, subscription_id)

    # Create Package
    print("Creating Package...")
    timestamp = time.strftime("%m%d%H%M", time.localtime())
    application_name = "contoso_package"
    version = timestamp
    package_name = "{name}-{version}".format(name=application_name, version = version)

    target_os_info_su = _get_target_os_info("Security updates")
    target_os_info_fu = _get_target_os_info("Feature updates")

    blob_path = _get_package_blob_path(resource_group, testbase_account_name, package_file_path, testbase_client)

    install_command = Command(name="install", action="Install", content_type="Path",
                              content="app/scripts/install/job.ps1",
                              run_elevated=False, restart_after=True,
                              max_run_time=1800, run_as_interactive=True,
                              always_run=True, apply_update_before=False)

    launch_command = Command(name="launch", action="Launch", content_type="Path",
                             content="app/scripts/launch/job.ps1",
                             run_elevated=True, restart_after=False,
                             max_run_time=1800, run_as_interactive=True,
                             always_run=False, apply_update_before=True)

    close_command = Command(name="close", action="Close", content_type="Path",
                            content="app/scripts/close/job.ps1",
                            run_elevated=True, restart_after=False,
                            max_run_time=1800, run_as_interactive=True,
                            always_run=False, apply_update_before=False)

    uninstall_command = Command(name="uninstall", action="Uninstall", content_type="Path",
                                content="app/scripts/uninstall/job.ps1",
                                run_elevated=True, restart_after=False,
                                max_run_time=1800, run_as_interactive=True,
                                always_run=True, apply_update_before=False)

    oob_test = Test(test_type="OutOfBoxTest",
                    commands=[install_command, launch_command, close_command, uninstall_command], is_active=True)

    package_resource = PackageResource(location="Global", tags={"client":"python-sdk"}, application_name=application_name,
                                     version=version, target_os_list=[
                                         target_os_info_su, target_os_info_fu],
                                     flighting_ring="Insider Beta Channel", blob_path=blob_path,
                                     tests=[oob_test])

    testbase_client.packages.begin_create(
        resource_group, testbase_account_name, package_name, package_resource)

    get_package_result = testbase_client.packages.get(
        resource_group, testbase_account_name, package_name)
    print(format_json(get_package_result))

def _get_package_blob_path(resource_group, testbase_account_name, package_file_path, testbase_client):
    file_upload_url_parameters = GetFileUploadURLParameters(
        blob_name="package.zip")
    file_upload_url_response = testbase_client.test_base_accounts.get_file_upload_url(
        resource_group, testbase_account_name, file_upload_url_parameters)
    blob_path = file_upload_url_response.blob_path
    upload_url = file_upload_url_response.upload_url

    storage_blob_client = BlobClient.from_blob_url(upload_url)
    with open(package_file_path, "rb") as data:
        storage_blob_client.upload_blob(data)

    blob_path = upload_url.split(".zip")[0]+".zip"
    return blob_path

def _get_target_os_info(update_type):
    if (update_type == "Security updates"):
        target_oss = ["Windows 10 21H1", "Windows 10 20H2", "Windows 10 1909", "All Future OS Updates",
                    "Windows Server 2019", "Windows Server 2019 - Server Core", "Windows Server 2016", "Windows Server 2016 - Server Core"]
        return TargetOSInfo(
            os_update_type="Security updates", target_o_ss=target_oss)
    else:
        return TargetOSInfo(os_update_type="Feature updates", target_o_ss=["Windows 10 21H2"])

if __name__ == "__main__":
    main()

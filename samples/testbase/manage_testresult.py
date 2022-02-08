# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

# Use `from azure.identity import AzureCliCredential` if authenticating via Azure CLI for test
from azure.identity import DefaultAzureCredential
from azure.identity import AzureCliCredential
from azure.mgmt.testbase import TestBase
from testbase_util import *

test_summary_format = """
{test_summary_name}
\tname:\t\t{application_name}
\tversion:\t{application_version}
\tstatus:\t\t{test_status}
\tgrade:\t\t{grade}
\ttestRunTime:\t{test_run_time}
"""

test_result_format = """
\ttestType:\t{test_type}
\trunTime:\t{test_run_time}
\tosName:\t\t{os_name}
\trelease:\t{release_name}
\tversion:\t{build_version}
\trevision:\t{build_revision}
"""

analysis_sumary_format = "\t\t\t{name}-{status}-{grade}"

def main():
    # Requesting token from Azure
    print("##Requesting token from Azure...")
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    #     Use `credential = AzureCliCredential()` if authenticating via Azure CLI for test
    credential = DefaultAzureCredential()

    # Run `export SUBSCRIPTION_ID="<subscription-id>"` on Linux-based OS
    # Run `set SUBSCRIPTION_ID=<subscription-id>` on Windows
    subscription_id = os.environ.get("SUBSCRIPTION_ID", None)

    # Set variables
    resource_group = "<resource-group-name>" # replace with real resource group name
    testBaseAccount_name = "<testbaseaccount-name>" # replace with real test base account name
    package_name = "<package-name>" # replace with real package name

    # Create client
    testbase_client = TestBase(credential, subscription_id)

    # Get test summary
    print("##Getting test summaries...")
    _print_test_summary_list(testbase_client, resource_group, testBaseAccount_name)

    # Get test result
    print("##Getting test result...")
    update_type = "SecurityUpdate" # replace with real update type
    filter_string = "osName eq 'Windows Server 2019' and releaseName eq '2021.09 B' and buildRevision eq '2178'" # replace with real filter for the test result
    _print_test_result_list(testbase_client, resource_group, testBaseAccount_name, package_name, update_type, filter_string)

def _print_test_summary_list(testbase_client, resource_group, testBaseAccount_name):
    test_summary_list = testbase_client.test_summaries.list(
        resource_group, testBaseAccount_name)
    if test_summary_list:
        for item in test_summary_list:
            test_summary_name = item.name
            test_summary_get = testbase_client.test_summaries.get(resource_group, testBaseAccount_name, test_summary_name)
            print(test_summary_format.format(
                test_summary_name=test_summary_name,
                application_name=test_summary_get.application_name,
                application_version=test_summary_get.application_version,
                test_status=test_summary_get.test_status,
                grade=test_summary_get.grade,
                test_run_time=test_summary_get.test_run_time))
            print("\tsecurityUpdate:")
            for su in test_summary_get.security_updates_test_summary.os_update_test_summaries:
                print("\t\t\t{os}-{build}-{status}-{grade}".format(os=su.os_name, build=su.build_version, status=su.execution_status, grade=su.grade))

def _print_test_result_list(testbase_client, resource_group, testBaseAccount_name, package_name, update_type, query_string):
    test_result_list = testbase_client.test_results.list(resource_group, testBaseAccount_name, package_name, update_type, query_string)
    if test_result_list:
        for result in test_result_list:
            test_result_name = result.name
            print(test_result_name)
            test_result = testbase_client.test_results.get(resource_group, testBaseAccount_name, package_name, test_result_name)
            print(test_result_format.format(
                test_type=test_result.test_type,
                test_run_time=test_result.test_run_time,
                os_name=test_result.test_run_time,
                release_name=test_result.release_name,
                build_version=test_result.build_version,
                build_revision=test_result.build_revision))
            print("\tanalysisSummaries:")
            for analysis in test_result.analysis_summaries:
                print(analysis_sumary_format.format(name=analysis.name, status=analysis.analysis_status, grade=analysis.grade))

if __name__ == "__main__":
    main()

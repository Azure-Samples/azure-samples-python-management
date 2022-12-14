# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient


def main():
    credentials = DefaultAzureCredential()
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    monitor_client = MonitorManagementClient(credentials, SUBSCRIPTION_ID)

    result = monitor_client.metrics.list(
        resource_uri="resourceUri",
        # timespan="2022-12-14T05:38:44Z/2022-12-14T06:38:44Z",
        timespan="timeSpan",
        # metricnamespace="Microsoft.Storage/storageAccounts",
        metricnamespace="metricNamespace",
        # filter="dim eq 'AccountResourceId'",
        filter="dim eq 'type'",
        top=3,
        orderby="Average asc",
        aggregation="Average,count",
        interval="PT1H"
    )
    print(result)


if __name__ == '__main__':
    main()

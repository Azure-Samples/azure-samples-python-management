import os
import json
from typing import Optional, List

from azure.identity import DefaultAzureCredential
from msrest import serialization


def send_request(client, next_link=None):
    headers = {"Accept": client._serialize.header("accept", "application/json", "str")}
    if not next_link:
        params = {"api-version": client._serialize.query("api_version", "2015-01-01", "str")}
        path_format_arguments = {
            'subscriptionId': client._serialize.url(
                "self._config.subscription_id", client._config.subscription_id, 'str'
            ),
        }
        url = "/subscriptions/{subscriptionId}/providers/Microsoft.ResourceHealth/availabilityStatuses"
        url = client._client.format_url(url, **path_format_arguments)
    else:
        url = next_link
        params = {}

    http_request = client._client.get(url=url, params=params, headers=headers)
    pipeline_response = client._client._pipeline.run(request=http_request, stream=False)
    return client._deserialize("AvailabilityStatusListResult", pipeline_response)


def print_result(result: List[serialization.Model]):
    print(f"there are {len(result)} items:")
    for item in result:
        print(json.dumps(item.serialize()))


def list1():
    sub_id = os.environ.get("SUBSCRIPTION_ID", None)
    from azure.mgmt.resourcehealth import MicrosoftResourceHealth
    client = MicrosoftResourceHealth(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )
    result = list(client.availability_statuses.list_by_subscription_id())
    print_result(result)


def list2():
    sub_id = os.environ.get("SUBSCRIPTION_ID", None)
    from azure.mgmt.resourcehealth.v2015_01_01 import MicrosoftResourceHealth
    client = MicrosoftResourceHealth(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )
    response = send_request(client)
    result = response.value
    while response.next_link:
        response = send_request(client, response.next_link)
        result.extend(response.value)
    print_result(result)


def main():
    ### There are 2 ways to list the resources with SDK ###

    # Solution 1: call operation directly (recommended)
    list1()

    # Solution 2 DIY HttpRequest (not recommended)
    # Only when solution 1 fails, you can try this solution
    list2()


if __name__ == "__main__":
    main()

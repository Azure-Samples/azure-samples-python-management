import os
import json

from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcehealth import MicrosoftResourceHealth


# - other dependence -
# - end -


def main():
    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resourcehealth_client = MicrosoftResourceHealth(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ.get("SUBSCRIPTION_ID", None)
    )
    # - init depended client -
    # - end -

    availability_statuses_list = resourcehealth_client.availability_statuses.list_by_subscription_id()
    for item in availability_statuses_list:
        print(json.dumps(item.serialize()))


if __name__ == "__main__":
    main()

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcehealth import MicrosoftResourceHealth


# - other dependence -
# - end -


def main(args):
    # SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)


    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resourcehealth_client = MicrosoftResourceHealth(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    availability_statuses_list = resourcehealth_client.availability_statuses.list_by_subscription_id()
    for availability_statuses in availability_statuses_list:
        print(availability_statuses)
        print(availability_statuses.properties)


if __name__ == "__main__":
    main()
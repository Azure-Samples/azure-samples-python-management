import os
import json

from azure.identity import DefaultAzureCredential
from azure.mgmt.reservations import AzureReservationAPI


def main():
    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    client = AzureReservationAPI(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ.get("SUBSCRIPTION_ID", None)
    )

    result = client.operation.list()
    for item in result:
        print(json.dumps(item.serialize()))


if __name__ == "__main__":
    main()

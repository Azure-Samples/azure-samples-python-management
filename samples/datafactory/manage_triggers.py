import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():
    credentials = DefaultAzureCredential()
    subscription = os.getenv('AZURE_SUBSCRIPTION_ID')
    resource_group_name = "exampleResourceGroup"
    factory_name = "exampleFactoryName"
    trigger_name = "exampleTrigger"

    # Create client
    datafactory_client = DataFactoryManagementClient(credentials, subscription)
    resource_client = ResourceManagementClient(credentials, subscription)

    # Create resource group
    resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": "eastus"}
    )

    # Create trigger
    response = datafactory_client.triggers.create_or_update(
        resource_group_name=resource_group_name,
        factory_name=factory_name,
        trigger_name=trigger_name,
        trigger={
            "properties": {
                "pipelines": [
                    {
                        "parameters": {"OutputBlobNameList": ["exampleoutput.csv"]},
                        "pipelineReference": {"referenceName": "examplePipeline", "type": "PipelineReference"},
                    }
                ],
                "type": "ScheduleTrigger",
                "typeProperties": {
                    "recurrence": {
                        "endTime": "2018-06-16T00:55:13.8441801Z",
                        "frequency": "Minute",
                        "interval": 4,
                        "startTime": "2018-06-16T00:39:13.8441801Z",
                        "timeZone": "UTC",
                    }
                },
            }
        },
    )
    print(response)

    # get trigger
    trigger = datafactory_client.triggers.get(
        resource_group_name=resource_group_name,
        factory_name=factory_name,
        trigger_name=trigger_name,
    )
    print(trigger)

    # start trigger
    start_response = datafactory_client.triggers.begin_start(
        resource_group_name=resource_group_name,
        factory_name=resource_group_name,
        trigger_name=trigger_name,
    ).result()
    print(start_response)

    # query by factory
    response = datafactory_client.triggers.query_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name,
        filter_parameters={"parentTriggerName": "exampleTrigger"},
    )
    print(response)

    # delete trigger
    datafactory_client.triggers.delete(
        resource_group_name=resource_group_name,
        factory_name=resource_group_name,
        trigger_name=trigger_name,
    )

    # Delete Group
    resource_client.resource_groups.begin_delete(
        resource_group_name
    ).result()


if __name__ == '__main__':
    main()

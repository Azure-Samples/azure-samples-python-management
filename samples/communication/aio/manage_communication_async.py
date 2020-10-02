# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import sys
import asyncio
import os
import argparse

from collections import namedtuple
from random import randint
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import ClientSecretCredential
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.communication.aio import CommunicationServiceManagementClient
from azure.mgmt.communication.models import CommunicationServiceResource
from azure.mgmt.communication.models import KeyType
from azure.mgmt.communication.models import TaggedResource
from azure.mgmt.communication.models import RegenerateKeyParameters

def __create_service_principal_credentials():
    """
    Create a ServicePrincipalCredentials object using values from environment variables
    For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    """

    # service principal's app id; `<your-app-id>`
    app_id = os.environ.get("AZURE_CLIENT_ID", None)
    # one of the service principal's client secrets; `<your-password>`
    client_secret = os.environ.get("AZURE_CLIENT_SECRET", None)
    # id of the principal's Azure Active Directory tenant; `<your-tenant-id>`
    tenant_id = os.environ.get("AZURE_TENANT_ID", None)

    if app_id is None or client_secret is None or tenant_id is None:
        return None

    return ClientSecretCredential(client_id=app_id, client_secret=client_secret, tenant_id=tenant_id)

def __create_resource_management_client(credential):
    """
    Create a ResourceManagementClient object using the subscription ID from environment variables
    """

    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    if subscription_id is None:
        return None

    return ResourceManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

def __create_communication_management_client(credentials):
    """
    Create a CommunicationServiceManagementClient object using a Subscription ID in an environment variable
    """

    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    if subscription_id is None:
        return None

    return CommunicationServiceManagementClient(credentials, subscription_id)


def __print_resource(resource):
    print("Name: " + resource.name)
    print("Provisioning State: " + resource.provisioning_state)
    print("Immutable Resource ID: " + resource.immutable_resource_id)
    print("Location: " + resource.location)
    print("Data Location: " + resource.data_location)
    print("Notification Hub ID: " + str(resource.notification_hub_id))
    print("Tags: " + str(resource.tags))

async def __create_communication_service(clients, args):
    """
    Create a Communication Service
    """
    print("\nCreate...")

    resource = CommunicationServiceResource(location="global", data_location = "UnitedStates")
    async_poller = await clients.acs_client.communication_service.begin_create_or_update(args.resource_group_name, args.resource_name, resource)

    print("Issued Create command. Waiting for response...")
    resource = await async_poller.result()
    print("Resource Created: ")
    __print_resource(resource)

async def __get_communication_service(clients, args):
    """
    Fetch a Communication Service
    """
    print("\nGet...")

    try:
        resource = await clients.acs_client.communication_service.get(args.resource_group_name, args.resource_name)
        __print_resource(resource)
    except HttpResponseError:
        print("Resource was not found.")

async def __update_communication_service(clients, args):
    """
    Update a Communication Service
    """
    print("\nUpdate...")

    tags = {}
    if args.keyvalues is not None:
        tags = {"tags": dict(args.keyvalues)}

    resource = await clients.acs_client.communication_service.update(args.resource_group_name, args.resource_name, TaggedResource(**tags))
    print("Resource Updated: ")
    __print_resource(resource)

async def __delete_communication_service(clients, args):
    """
    Delete a Communication Service
    """
    print("\nDelete...")

    await clients.acs_client.communication_service.begin_delete(args.resource_group_name, args.resource_name)

async def __list_communication_service_by_subscription(clients, args):
    """
    List all Communication Services in the subscription
    """
    print("\nList by subscription...")

    resources = clients.acs_client.communication_service.list_by_subscription()
    print("Found resources: ")
    async for resource in resources:
        print("")
        __print_resource(resource)

async def __list_communication_service_by_resource_group(clients, args):
    """
    List all Communication Services in the resource group
    """
    print("\nList by resource group...")

    resources = clients.acs_client.communication_service.list_by_resource_group(args.resource_group_name)
    print("Found resources: ")
    async for resource in resources:
        print("")
        __print_resource(resource)

async def __list_keys(clients, args):
    """
    List the Primary and Secondary key pairs
    """
    print("\nList keys...")

    keys = await clients.acs_client.communication_service.list_keys(args.resource_group_name, args.resource_name)
    print(keys)


async def __regenerate_key(clients, args):
    """
    Regenerate the Primary or Secondary key pair
    """
    print("\nRegeneration key...")

    key_type = {"key_type": args.type}
    key = await clients.acs_client.communication_service.regenerate_key(args.resource_group_name, args.resource_name, RegenerateKeyParameters(**key_type))
    print(key)

async def __link_notification_hub(clients, args):
    """
    Link a Notification Hub to the Communication Service
    """
    print("\nLink Notification Hub...")

    # Resource ID of the Notification Hub you want to  link; `<your-tenant-id>`
    notification_hub_resource_id = os.environ.get("AZURE_NOTIFICATION_HUB_ID", None)
    # Connection String of the Notification Hub you want to  link; `<your-tenant-id>`
    notification_hub_connection_string = os.environ.get("AZURE_NOTIFICATION_HUB_CONNECTION_STRING", None)

    if notification_hub_resource_id is None or notification_hub_connection_string is None:
        return None

    linked_notification_hub = await clients.acs_client.communication_service.link_notification_hub(args.resource_group_name, args.resource_name, { 'resource_id': notification_hub_resource_id, 'connection_string': notification_hub_connection_string })
    print("Linked: ")
    print(linked_notification_hub)

async def __create_resource_group(clients, args):
    """
    Create a Resource Group for the given name
    """

    await clients.resource_client.resource_groups.create_or_update(
        args.resource_group_name,
        {"location": "westus"}
    )

async def __delete_resource_group(clients, args):
    """
    Create a Resource Group for the given name
    """

    await clients.resource_client.resource_groups.begin_delete(
        args.resource_group_name
    )

async def __resource_group_exists(clients, args):
    """
    Check if the given Resource Group Exists
    """

    try:
        await clients.resource_client.resource_groups.get(args.resource_group_name)
    except ResourceNotFoundError:
        return False

    return True

async def __run_all(clients, args):
    """
    Run all available commands for Communication Services
    """

    resource_group_exists = await __resource_group_exists(clients, args)

    # Ensure Resource Group Exists
    if resource_group_exists is False:
        await __create_resource_group(clients, args)

    # Run through all API calls
    await __create_communication_service(clients, args)
    await __get_communication_service(clients, args)
    await __update_communication_service(clients, args)

    await __list_communication_service_by_subscription(clients, args)
    await __list_communication_service_by_resource_group(clients, args)

    await __list_keys(clients, args)
    await __regenerate_key(clients, args)

    await __delete_communication_service(clients, args)

    # Clean up created Resource Group
    if resource_group_exists is False:
        await __delete_resource_group(clients, args)

def __setup_create_communication_service(subparsers, parent_parser):
    """
    Define the parser for the create command.
    """

    parser = subparsers.add_parser('create', help='Create a Communication Service')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.set_defaults(func=__create_communication_service)

def __setup_get_communication_service(subparsers, parent_parser):
    """
    Define the parser for the get command.
    """

    parser = subparsers.add_parser('get', help='Fetch a Communication Service')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.set_defaults(func=__get_communication_service)

def __setup_update_communication_service(subparsers, parent_parser):
    """
    Define the parser for the update command. Provide the tags like so: "--keyvalue foo1=bar1 --keyvalue foo2=bar2"
    """

    parser = subparsers.add_parser('update', help='Update a Communication Service')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.add_argument("--keyvalue", action='append', type=lambda kv: kv.split("="), dest='keyvalues')

    parser.set_defaults(func=__update_communication_service)

def __setup_delete_communication_service(subparsers, parent_parser):
    """
    Define the parser for the delete command.
    """

    parser = subparsers.add_parser('delete', help='Delete a Communication Service')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.set_defaults(func=__delete_communication_service)

def __setup_list_communication_service_by_subscription(subparsers, parent_parser):
    """
    Define the parser for the list command.
    """

    parser = subparsers.add_parser('list', help='List all Communication Services in the subscription')
    parser.set_defaults(func=__list_communication_service_by_subscription)

def __setup_list_communication_service_by_resource_group(subparsers, parent_parser):
    """
    Define the parser for the list command.
    """

    parser = subparsers.add_parser('list-by-rg', help='List all Communication Services in the resource group')
    parser.add_argument('resource_group_name', type=str)
    parser.set_defaults(func=__list_communication_service_by_resource_group)

def __setup_list_keys(subparsers, parent_parser):
    """
    Define the parser for the list keys command.
    """

    parser = subparsers.add_parser('list-keys', help='List the Primary and Secondary key pairs')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.set_defaults(func=__list_keys)

def __setup_regenerate_key(subparsers, parent_parser):
    """
    Define the parser for the regenerate key command.
    """

    parser = subparsers.add_parser('regenerate-key', help='Regenerate the Primary or Secondary key pair')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.add_argument('type', type=str, choices=['Primary', 'Secondary'])
    parser.set_defaults(func=__regenerate_key)


def __setup_link_notification_hub(subparsers, parent_parser):
    """
    Define the parser for the link notification hub command.
    """

    parser = subparsers.add_parser('link-notification-hub', help='Link a Notification Hub to the Communication Service')
    parser.add_argument('resource_group_name', type=str)
    parser.add_argument('resource_name', type=str)
    parser.set_defaults(func=__link_notification_hub)

def __setup_run_all(subparsers, parent_parser):
    """
    Define the parser to run all commands.
    """

    resource_name = "py-sample-" + str(randint(1, 1000000))
    resource_group_name = "rg-py-sample-" + str(randint(1, 1000000))

    parser = subparsers.add_parser('all', help='Run all available commands for Communication Services')
    parser.add_argument('resource_group_name', type=str, nargs='?', default=resource_group_name)
    parser.add_argument('resource_name', type=str, nargs='?', default=resource_name)
    parser.add_argument('type', type=str, nargs='?', choices=['Primary', 'Secondary'], default='Primary')
    parser.add_argument("--keyvalue", action='append', type=lambda kv: kv.split("="), dest='keyvalues')
    parser.set_defaults(func=__run_all)

async def main():
    """Main"""

    """Parse arguments"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    __setup_create_communication_service(subparsers, parser)
    __setup_get_communication_service(subparsers, parser)
    __setup_update_communication_service(subparsers, parser)
    __setup_delete_communication_service(subparsers, parser)
    __setup_list_communication_service_by_subscription(subparsers, parser)
    __setup_list_communication_service_by_resource_group(subparsers, parser)
    __setup_list_keys(subparsers, parser)
    __setup_regenerate_key(subparsers, parser)
    __setup_link_notification_hub(subparsers, parser)
    __setup_run_all(subparsers, parser)

    args = parser.parse_args()

    Clients = namedtuple('Clients', 'resource_client acs_client')

    credential = __create_service_principal_credentials()
    if credential is None:
        raise Exception("Failed to create service principal credentials")

    # Create all the clients
    resource_client = __create_resource_management_client(credential)
    if resource_client is None:
        raise Exception("Failed to create ResourceManagementClient")

    acs_client = __create_communication_management_client(credential)
    if acs_client is None:
        raise Exception("Failed to create CommunicationServiceManagementClient")

    clients = Clients(resource_client, acs_client)

    await args.func(clients, args)

    # [Warning] All clients and credentials need to be closed.
    # link: https://github.com/Azure/azure-sdk-for-python/issues/8990
    await credential.close()
    await resource_client.close()
    await acs_client.close()

    return 0


if __name__ == "__main__":
    # Fix for Windows - Python 3.8+ raises "RuntimeError: Event Loop is closed" on exit: https://github.com/encode/httpx/issues/914
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()


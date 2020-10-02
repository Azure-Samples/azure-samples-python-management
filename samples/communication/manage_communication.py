# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import argparse

from random import *
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.communication import CommunicationServiceManagementClient
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

def __create_resource_management_client():
    """
    Create a ResourceManagementClient object using the subscription ID from environment variables
    """

    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    if subscription_id is None:
        return None

    return ResourceManagementClient(
        credential=__create_service_principal_credentials(),
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


def __get_communication_management_client():
    """
    Create credential object and create a management client using it
    """

    credential = __create_service_principal_credentials()
    if credential is None:
        raise Exception("Failed to create service principal credentials")

    client = __create_communication_management_client(credential)
    if client is None:
        raise Exception("Failed to create CommunicationServiceManagementClient")

    return client

def __print_resource(resource):
    print("Name: " + resource.name)
    print("Provisioning State: " + resource.provisioning_state)
    print("Immutable Resource ID: " + resource.immutable_resource_id)
    print("Location: " + resource.location)
    print("Data Location: " + resource.data_location)
    print("Notification Hub ID: " + str(resource.notification_hub_id))
    print("Tags: " + str(resource.tags))

def __create_communication_service(args):
    """
    Create a Communication Service
    """
    print("\nCreate...")

    acs_client = __get_communication_management_client()
    resource = CommunicationServiceResource(location="global", data_location = "UnitedStates")
    operation = acs_client.communication_service.begin_create_or_update(args.resource_group_name, args.resource_name, resource)

    print("Issued Create command. Waiting for response...")
    resource = operation.result(timeout=1)
    print("Resource Created: ")
    __print_resource(resource)

def __get_communication_service(args):
    """
    Fetch a Communication Service
    """
    print("\nGet...")

    acs_client = __get_communication_management_client()

    try:
        resource = acs_client.communication_service.get(args.resource_group_name, args.resource_name)
        __print_resource(resource)
    except HttpResponseError:
        print("Resource was not found.")

def __update_communication_service(args):
    """
    Update a Communication Service
    """
    print("\nUpdate...")

    acs_client = __get_communication_management_client()

    tags = {}
    if args.keyvalues is not None:
        tags = {"tags": dict(args.keyvalues)}

    resource = acs_client.communication_service.update(args.resource_group_name, args.resource_name, TaggedResource(**tags))
    print("Resource Updated: ")
    __print_resource(resource)

def __delete_communication_service(args):
    """
    Delete a Communication Service
    """
    print("\nDelete...")

    acs_client = __get_communication_management_client()
    acs_client.communication_service.begin_delete(args.resource_group_name, args.resource_name)
    print("Resource Deleted")

def __list_communication_service_by_subscription(args):
    """
    List all Communication Services in the subscription
    """
    print("\nList by subscription...")

    acs_client = __get_communication_management_client()
    resources = acs_client.communication_service.list_by_subscription()
    print("Found resources: ")
    for resource in resources:
        print("")
        __print_resource(resource)

def __list_communication_service_by_resource_group(args):
    """
    List all Communication Services in the resource group
    """
    print("\nList by resource group...")

    acs_client = __get_communication_management_client()
    resources = acs_client.communication_service.list_by_resource_group(args.resource_group_name)
    print("Found resources: ")
    for resource in resources:
        print("")
        __print_resource(resource)

def __list_keys(args):
    """
    List the Primary and Secondary key pairs
    """
    print("\nList keys...")

    acs_client = __get_communication_management_client()
    keys = acs_client.communication_service.list_keys(args.resource_group_name, args.resource_name)
    print(keys)


def __regenerate_key(args):
    """
    Regenerate the Primary or Secondary key pair
    """
    print("\nRegeneration key...")

    acs_client = __get_communication_management_client()

    key_type = {"key_type": args.type}
    key = acs_client.communication_service.regenerate_key(args.resource_group_name, args.resource_name, RegenerateKeyParameters(**key_type))
    print(key)

def __link_notification_hub(args):
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

    acs_client = __get_communication_management_client()
    linked_notification_hub = acs_client.communication_service.link_notification_hub(args.resource_group_name, args.resource_name, { 'resource_id': notification_hub_resource_id, 'connection_string': notification_hub_connection_string })
    print("Linked: ")
    print(linked_notification_hub)

def __create_resource_group(args):
    """
    Create a Resource Group for the given name
    """

    resource_client = __create_resource_management_client()
    resource_client.resource_groups.create_or_update(
        args.resource_group_name,
        {"location": "westus"}
    ).result()

def __delete_resource_group(args):
    """
    Create a Resource Group for the given name
    """

    resource_client = __create_resource_management_client()
    resource_client.resource_groups.begin_delete(
        args.resource_group_name
    ).result()

def __resource_group_exists(args):
    """
    Check if the given Resource Group Exists
    """

    resource_client = __create_resource_management_client()

    try:
        resource_client.resource_groups.get(args.resource_group_name)
    except ResourceNotFoundError:
        return False

    return True

def __run_all(args):
    """
    Run all available commands for Communication Services
    """

    resource_group_exists = __resource_group_exists(args)

    # Ensure Resource Group Exists
    if resource_group_exists is False:
        __create_resource_group(args)

    # Run through all API calls
    __create_communication_service(args)
    __get_communication_service(args)
    __update_communication_service(args)

    __list_communication_service_by_subscription(args)
    __list_communication_service_by_resource_group(args)

    __list_keys(args)
    __regenerate_key(args)

    __delete_communication_service(args)

    # Clean up created Resource Group
    if resource_group_exists is False:
        __delete_resource_group(args)

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

def main():
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

    args.func(args)

    return 0


if __name__ == "__main__":
    exit(main())

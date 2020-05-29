# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    GALLERY_NAME = "galleryname"
    APPLICATION_NAME = "applicationname"
    IMAGE_NAME = "imagex"
    DISK_NAME = "diskname"
    SNAPSHOT_NAME = "snapshotname"
    VERSION_NAME = "1.0.0"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create disk
    disk = compute_client.disks.begin_create_or_update(
        GROUP_NAME,
        DISK_NAME,
        {
          "location": "eastus",
          "creation_data": {
            "create_option": "Empty"
          },
          "disk_size_gb": "200"
        }
    ).result()

    # Create snapshot
    snapshot = compute_client.snapshots.begin_create_or_update(
        GROUP_NAME,
        SNAPSHOT_NAME,
        {
          "location": "eastus",
          "creation_data": {
            "create_option": "Copy",
            "source_uri": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Compute/disks/" + DISK_NAME
          }
        }
    ).result()

    # Create gallery
    gallery = compute_client.galleries.begin_create_or_update(
        GROUP_NAME,
        GALLERY_NAME,
        {
          "location": "eastus",
          "description": "This is the gallery description."
        }
    ).result()
    print("Create gallery:\n{}".format(gallery))

    # Create gallery application
    application = compute_client.gallery_applications.begin_create_or_update(
        GROUP_NAME,
        GALLERY_NAME,
        APPLICATION_NAME,
        {
          "location": "eastus",
          "description": "This is the gallery application description.",
          "eula": "This is the gallery application EULA.",
          "supported_os_type": "Windows"
        }
    ).result()
    print("Create gallery application:\n{}".format(application))

    # Create gallery image
    image = compute_client.gallery_images.begin_create_or_update(
        GROUP_NAME,
        GALLERY_NAME,
        IMAGE_NAME,
        {
          "location": "eastus",
          "os_type": "Windows",
          "os_state": "Generalized",
          "hyper_vgeneration": "V1",
          "identifier": {
            "publisher": "myPublisherName",
            "offer": "myOfferName",
            "sku": "mySkuName"
          }
        }
    ).result()
    print("Create gallery image:\n{}".format(image))

    # Get gallery
    gallery = compute_client.galleries.get(
        GROUP_NAME,
        GALLERY_NAME
    )
    print("Get gallery:\n{}".format(gallery))

    # Get gallery application
    application = compute_client.gallery_applications.get(
        GROUP_NAME,
        GALLERY_NAME,
        APPLICATION_NAME
    )
    print("Get gallery application:\n{}".format(application))

    # Get gallery image
    image = compute_client.gallery_images.get(
        GROUP_NAME,
        GALLERY_NAME,
        IMAGE_NAME
    )
    print("Get gallery image:\n{}".format(image))

    # Update gallery
    gallery = compute_client.galleries.begin_update(
        GROUP_NAME,
        GALLERY_NAME,
        {
          "description": "This is the gallery description."
        }
    ).result()
    print("Update gallery:\n{}".format(gallery))

    # Update gallery application
    application = compute_client.gallery_applications.begin_update(
        GROUP_NAME,
        GALLERY_NAME,
        APPLICATION_NAME,
        {
          "description": "This is the gallery application description.",
          "eula": "This is the gallery application EULA.",
          "supported_os_type": "Windows",
          "tags": {
            "tag1": "tag1"
          }
        }
    ).result()
    print("Update gallery application:\n{}".format(application))

    # Update gallery image
    image = compute_client.gallery_images.begin_update(
        GROUP_NAME,
        GALLERY_NAME,
        IMAGE_NAME,
        {
          "os_type": "Windows",
          "os_state": "Generalized",
          "hyper_vgeneration": "V1",
          "identifier": {
            "publisher": "myPublisherName",
            "offer": "myOfferName",
            "sku": "mySkuName"
          }
        }
    ).result()
    print("Update gallery image:\n{}".format(image))

    # Delete gallery image
    compute_client.gallery_images.begin_delete(
        GROUP_NAME,
        GALLERY_NAME,
        IMAGE_NAME
    ).result()
    print("Delete gallery image.\n")

    # Delete gallery application
    compute_client.gallery_applications.begin_delete(
        GROUP_NAME,
        GALLERY_NAME,
        APPLICATION_NAME
    ).result()
    print("Delete gallery application.\n")

    # Delete gallery
    compute_client.galleries.begin_delete(
        GROUP_NAME,
        GALLERY_NAME
    ).result()
    print("Delete gallery.")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()

---
page_type: sample
languages:
- python
products:
- azure
description: "These code samples will show you how to manage Group Quota using Azure SDK for Python."
urlFragment: quota
---

# Getting started - Managing Group Quota using Azure Python SDK

These code samples will show you how to manage Group Quota using Azure SDK for Python.

## Features

This project framework provides examples for the following services:

### Quota
- Using the Azure SDK for Python - Quota Management Library [azure-mgmt-quota](https://pypi.org/project/azure-mgmt-quota/)

`pip install azure-mgmt-quota`

## Getting Started

### Prerequisites

1. Before we run the samples, we need to make sure we have setup the credentials. Follow the instructions in [register a new application using Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) to obtain `subscription id`,`client id`,`client secret`, and `application id`

2. Store your credentials an environment variables.
For example, in Linux-based OS, you can do
```bash
export AZURE_TENANT_ID="xxx"
export AZURE_CLIENT_ID="xxx"
export AZURE_CLIENT_SECRET="xxx"
```

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 3.7+.

2. Install the following specific SDK version, [Link to SDK 2.0.0b1](https://pypi.org/project/azure-mgmt-quota/2.0.0b1/)

### Quickstart

1.  Clone the repository.

    ```
    git clone https://github.com/Azure/azure-sdk-for-python.git
    ```

2.  Install the dependencies using pip.

    ```
    pip install azure-identity
    pip install azure-mgmt-quota
    ```

## Run

To run the script, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

1. `python put_group_quota_limits_requests_compute.py`

Allocate Quota to Group

1. `python put_subscription_quota_allocation_request_compute.py`

Allocate Quota to a Subscription in Group

## Resources

Link to full list of SDK scripts

- https://github.com/Azure/azure-sdk-for-python/tree/0a8dfb57ae574d38a304ca447957c27aa7224f2c/sdk/quota/azure-mgmt-quota/generated_samples
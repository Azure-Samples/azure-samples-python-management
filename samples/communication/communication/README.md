---
page_type: sample
languages:
- python
products:
- azure
description: "These code samples will show you how to manage Communication Service resources using Azure SDK for Python."
urlFragment: communication
---

# Getting started - Managing Azure Communication Services using Azure Python SDK

These code samples will show you how to manage Communication Service resources using Azure SDK for Python.

## Features

This project framework provides examples for the following services:

### Communication

* Using the Azure SDK for Python - Communication Management Library [azure-mgmt-communication](https://pypi.org/project/azure-mgmt-communication/) for the [Azure Communication API](https://docs.microsoft.com/en-us/rest/api/communication/)

## Getting Started

### Prerequisites

1. Before we run the samples, we need to make sure we have setup the credentials. Follow the instructions in
   [register a new application using Azure
   portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
   to obtain `subscription id`,`client id`,`client secret`, and `application id`

2. Store your credentials an environment variables.
For example, in Linux-based OS, you can do

```bash
export AZURE_TENANT_ID="xxx"
export AZURE_CLIENT_ID="xxx"
export AZURE_CLIENT_SECRET="xxx"
export AZURE_SUBSCRIPTION_ID="xxx"
export AZURE_NOTIFICATION_HUB_ID="xxx"
export AZURE_NOTIFICATION_HUB_CONNECTION_STRING="xxx"
```

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2.  General recommendation for Python development is to use a Virtual Environment.
    For more information, see https://docs.python.org/3/tutorial/venv.html

    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install
    [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

### Quickstart

1.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/azure-samples-python-management.git
    ```

2.  Install the dependencies using pip.

    ```
    cd azure-samples-python-management/samples/communication
    pip install -r requirements.txt
    ```

## Demo

A demo app is included to show how to use the project.

To view all available commands for the demo, execute `python manage_communication.py -h`

To run the complete demo, execute `python manage_communication.py all`


The sample files do not have dependency each other and each file represents an individual end-to-end scenario. Please look at the sample that contains the scenario you are interested in

## Resources

- https://github.com/Azure/azure-sdk-for-python

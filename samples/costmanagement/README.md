---
page_type: sample
languages:
- python
products:
- azure
description: "These code samples will show you how to manage Consumption using Azure SDK for Python."
urlFragment: costmanagement
---

# Getting started - Managing Consumption using Azure Python SDK

These code samples will show you how to manage costmanagement using Azure SDK for Python.

## Features

This project framework provides examples for the following services:

### costmanagement
* [] Using the Azure SDK for Python - costmanagement Management Library [azure-mgmt-costmanagement](https://pypi.org/project/azure-mgmt-costmanagement/) for the [costmanagement API](https://docs.microsoft.com/en-us/rest/api/cost-management/)

## Getting Started

### Prerequisites

1. Before we run the samples, we need to make sure we have setup the credentials. Follow the instructions in [register a new application using Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) to obtain `subscription id`,`client id`,`client secret`, and `application id`

2. Store your credentials an environment variables.
For example, in Linux-based OS, you can do
```bash
export AZURE_TENANT_ID="xxx"
export AZURE_CLIENT_ID="xxx"
export AZURE_CLIENT_SECRET="xxx"
export AZURE_SUBSCRIPTION_ID="xxx"
```

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 3.6+.

2.  General recommendation for Python development is to use a Virtual Environment.
    For more information, see https://docs.python.org/3/tutorial/venv.html

    Install and initialize the virtual environment with the "venv" module on Python 3.6+:

    ```
    python -m venv mytestenv # Might be "python3" or "py3.6" depending on your Python installation
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
    cd azure-samples-python-management/samples/costmanagement
    pip install -r requirements.txt
    ```

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

1. `python manage_workspace.py`

If the script starts with `disable_***.py`, it means that it is unavailable now.

The sample files do not have dependency each other and each file represents an individual end-to-end scenario. Please look at the sample that contains the scenario you are interested in

## Resources

- https://github.com/Azure/azure-sdk-for-python

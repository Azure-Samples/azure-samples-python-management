---
page_type: sample
languages:
- python
products:
- azure
description: "These samples will show you how to show to manage Redis using Azure Python SDK."
urlFragment: redis
---

# Getting started - Managing Redis using Azure Python SDK

These samples will show you how to show to manage Redis using Azure Python SDK.

## Features

This project framework provides examples for the following services:

### Redis
* Using the Azure SDK for Python - Redis Management Library [azure-mgmt-redis](https://pypi.org/project/azure-mgmt-redis/) for the [Azure Redis Management API](https://docs.microsoft.com/en-us/rest/api/redis/)

## Getting Started

### Prerequisites

1. Before we run the samples, we need to make sure we have setup the credentials. Follow the instructions in [register a new application using Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) to obtain `subscription id`,`client id`,`client secret`, and `application id`

2. Store your credentials an environment variables.   
For example, in Linux-based OS, you can do
```bash
export AZURE_TENANT_ID="xxx"
export AZURE_CLIENT_ID="xxx"
export AZURE_CLIENT_SECRET="xxx"
export SUBSCRIPTION_ID="xxx"
```

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2.  General recommendation for Python development is to use a Virtual Environment.
    For more information, see https://docs.python.org/3/tutorial/venv.html

    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

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
    cd azure-samples-python-management/samples/redis
    pip install -r requirements.txt
    ```

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

1. `python manage_redis.py`

If the script starts with `disable_***.py`, it means that it is unavailable now.

Each file is a separate code sample that no dependency on other files. You can look at whichever code sample you're interested in

## Resources

- https://github.com/Azure/azure-sdk-for-python

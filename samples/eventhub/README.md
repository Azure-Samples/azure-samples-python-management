---
page_type: sample
languages:
- python
products:
- azure
description: "These samples will show you how to manage reosurce in eventhub sdk."
urlFragment: azure-samples-python-management
---

# Python Management SDK Samples

These samples will show you how to manage reosurces in eventhub sdk.

## Features

This project framework provides examples for the following services:

### Eventhub
* [] Using the **Management Eventhub SDK** [azure-mgmt-eventhub](https://pypi.org/project/azure-mgmt-eventhub/) for the [Eventhub API](https://docs.microsoft.com/en-us/rest/api/eventhub/)

## Getting Started

### Prerequisites

1.  Before we start these samples, we need [register a new application using Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal). Then copy the `Subscription ID`, `Application (client) ID`, `Directory (tenant) ID` and create a new application secret to get the secret value.

2. Put your secret info into environment. The example in linux bash:
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
    cd azure-samples-python-management/samples/eventhub
    pip install -r requirements.txt
    ```

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

1. `python manage_eventhub.py`
2. `python manage_consumer_groups.py`

If the script start with `disable_***.py`, it means that it is unavailable now.

To see the code of each example, simply look at the examples in the module folder. They are written to be isolated in scope so that you can see only what you're interested in.

## Resources

- https://github.com/Azure/azure-sdk-for-python

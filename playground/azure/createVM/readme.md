# How to run sample in track2

## 1. Install dependences for track2
run `pip install -r track2_requirements.txt`

## 2. create env values
We need put app registration information into env values.   
For example in linux:
```bash
export AZURE_TENANT_ID=""
export AZURE_CLIENT_ID=""
export AZURE_CLIENT_SECRET=""
export SUBSCRIPTION_ID=""
```

You can update env values in `env.sh` and run `source env.sh` to make it vailable in current shell.

About how to create app registration, see here: https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app

## 3. test sample
just run `track2.py` to test creating virtualmachine in track2 sdk.   
Atfter finish script, you can find your virtualmachine in azure portal.

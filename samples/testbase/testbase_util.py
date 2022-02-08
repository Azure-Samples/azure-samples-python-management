# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import json

def format_json(content):
    return json.dumps(content.serialize(keep_readonly=True), indent=4, separators=(',', ': '))

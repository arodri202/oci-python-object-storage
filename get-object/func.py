# Copyright (c) 2016, 2018, Oracle and/or its affiliates.  All rights reserved.
import io
import os
import json
import sys
from fdk import response

import oci.object_storage

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()

    try:
        body = json.loads(data.getvalue())
        bucketName = body["bucketName"]
        fileName = body["fileName"]

    except Exception as e:
        error = 'Input a JSON object in the format: \'{"bucketName": "<bucket name>"}, "fileName": "<filename>"}\' '
        raise Exception(error)

    resp = do(signer, bucketName, fileName)

    return response.Response(
        ctx, response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def do(signer, bucketName, fileName):
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    message = "Failed: The object " + str(fileName) + " could not be retrieved."

    try:
        print("Searching for bucket and object", file=sys.stderr)
        object = client.get_object(os.environ.get("OCI_NAMESPACE"), bucketName, fileName)

        print("found object", file=sys.stderr)
        if object.status == 200:
            message = "Success: The object " + str(fileName) + " was retrieved, content: " + str(object.data.text)

    except Exception as e:
        message = "Failed: " + str(e.message)

    response = {
        "content": message
    }
    return response

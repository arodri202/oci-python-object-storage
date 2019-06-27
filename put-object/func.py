import io
import os
import json
import sys
from fdk import response

import oci.object_storage

sys.path.append(".")
import rp
# get
def handler(ctx, data: io.BytesIO=None):
    provider = rp.MockResourcePrincipalProvider() # initialized provider here

    try:
        body = json.loads(data.getvalue())
        bucketName = body.get("bucketName")
        fileName = body.get("fileName")
        content = body.get("content")

    except Exception as e:
        error = 'Input a JSON object in the format: \'{"bucketName": "<bucket name>"}\' , "content": "<content>"}\' '
        return response.Response(
        ctx, response_data=json.dumps(
            {"error": error}),
        headers={"Content-Type": "application/json"}
        )
    resp = do(provider, bucketName, fileName, content)

    return response.Response(
        ctx, response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def do(provider, bucketName, fileName, content):
    client = oci.object_storage.ObjectStorageClient(provider.config, signer=provider.signer)
    try:
        object = client.put_object(os.environ.get("OCI_NAMESPACE"), bucketName, fileName, json.dumps(content))
        output = "Success: Put object '" + fileName + "' in bucket '" + bucketName + "'"
    except Exception as e:
        output = "Failed: " + str(e.message)

    response = {
        "state": output,
    }
    return response

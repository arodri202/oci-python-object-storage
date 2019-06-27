# Using Environmental Variables to Access Object Storage with the OCI Python SDK

  This function uses Environmental Configuration to gain access to OCI's Object Storage.

  Uses the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html) to create a client that gets access to OCI Object Storage.

  As you make your way through this tutorial, look out for this icon. ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE) Whenever you see it, it's time for you to perform an action.


Pre-requisites:
---------------
  1. Start by making sure all of your policies are correct from this [guide](https://preview.oci.oraclecorp.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

  2. Have a valid config file in ~/.oci/config, if you do not already have one, follow [this guide](https://docs.cloud.oracle.com/iaas/Content/API/Concepts/sdkconfig.htm) to create one.

  3. Download [rp.py](https://github.com/arodri202/oci-python-object-storage/blob/master/put-object/rp.py) and [setup_config.sh](https://github.com/arodri202/oci-python-object-storage/blob/master/setup_config.sh) move it into your working directory.

  4. Have [Fn CLI setup with Oracle Functions](https://preview.oci.oraclecorp.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

### Switch to the correct context
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  fn use context <your context name>
  ```
  Check using
  ```
  fn ls apps
  ```

### Create your Environmental Variables

  Give executable and source permissions to `setup_config.sh`, and run the script which reads your config file at `~/.oci/config` to setup your environmental variables.
  ```
  chmod 744 setup_config.sh
  source setup_config.sh
  ./setup_config
  ```


### Create or Update your Dynamic Groups
  In order to use and retrieve information about other OCI Services you must grant access to your Function via a dynamic group. For information on how to create a dynamic group, click [here.](https://preview.oci.oraclecorp.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To)

  When specifying a rule, consider the following examples:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  * If you want all functions in a compartment to be able to access a resource, enter a rule similar to the following that adds all functions in the compartment with the specified compartment OCID to the dynamic group:
  ```
  ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
  ```

  * If you want a specific function to be able to access a resource, enter a rule similar to the following that adds the function with the specified OCID to the dynamic group:
  ```
  resource.id = 'ocid1.fnfunc.oc1.iad.aaaaaaaaacq______dnya'
  ```

### Create or Update Policies
  Now that your dynamic group is created, create a new policy that allows your new dynamic group to inspect any resources you are interested in receiving information about, in this case we will grant access to `object-family` in the functions related compartment.

  Your policy should look something like this:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  Allow dynamic-group <your dynamic group name> to inspect object-family in compartment <your compartment name>
  ```
  e.g.
  ```
  Allow dynamic-group demo-func-dyn-group to inspect object-family in compartment demo-func-compartment
  ```

  For more information on how to create policies, go [here.](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm)


Create your application environment
------------------
  Get the python boilerplate by running:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  mkdir <directory-name>
  ```
  e.g.
  ```
  mkdir python-object-storage
  ```

  Enter the directory and create an `app.yaml` file to denote that this is an application directory and not a function directory.
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  echo "name: <app-name>" >> app.yaml
  ```
  e.g.
  ```
  echo "name: python-object-storage" >> app.yaml
  ```

  Now, we can initialize our functions, in this tutorial we will have two functions, one to list objects in a bucket, and one to put objects in a bucket.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  fn init --runtime python <function-name>
  ```
  e.g.
  ```
  fn init --runtime python list-objects
  fn init --runtime python put-objects
  ```

  This will make two boilerplates in separate directories within your project folder. Make sure both directories have a copy of `rp.py` and an `__init__.py`

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  touch put-objects/__init__.py
  touch list-objects/__init__.py
  cp rp.py put-objects
  cp rp.py list-objects
  ```

### Create an Application that is connected to Oracle Functions with Required Configuration
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]' --config TENANCY=<TENANCY_OCID> --config USER=<USER_OCID --config FINGERPRINT=<PUBLIC_KEY_FINGERPRINT> --config PASSPHRASE=<PASSPHRASE> --config REGION=<OCI_REGION> --config NAMESPACE=<NAMESPACE>
  ```

  You can find the subnet-ocid by logging on to [cloud.oracle.com](https://cloud.oracle.com/en_US/sign-in), navigating to Core Infrastructure > Networking > Virtual Cloud Networks. Make sure you are in the correct Region and Compartment, click on your VNC and select the subnet you wish to use. Since we ran the `setup_config.sh` script, we can use the variables we already created from your config file so you don't have to do any searching.

  e.g.
  ```
  fn create app python-object-storage --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]' --config OCI_USER=$OCI_USER --config OCI_FINGERPRINT=$OCI_FINGERPRINT --config OCI_TENANCY=$OCI_TENANCY --config OCI_PRIVATE_KEY_PASS=$OCI_PRIVATE_KEY_PASS --config OCI_REGION=$OCI_REGION --config OCI_NAMESPACE=$OCI_NAMESPACE
  ```

Writing the Function
------------------
These next steps are needed for every function so make sure to update this for as many functions as you create
### Requirements
  Update your requirements.txt file to contain the following:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  fdk
  oci-cli
  ```

### Open func.py
  Update the imports so that you contain the following.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```python
  import io
  import json
  import os
  import sys
  from fdk import response

  import oci.object_storage

  sys.path.append(".")
  import rp
  ```

  By calling `sys.path.append(".")` the Python interpreter is able to import the `rp.py` Python module in your directory that you downloaded earlier.

## List Objects
 Handler method
  This is what is called when the function is invoked by Oracle Functions, delete what is given from the boilerplate and update it to contain the following:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```python
  def handler(ctx, data: io.BytesIO=None):
      provider = rp.MockResourcePrincipalProvider() # initialized provider here
      try:
          body = json.loads(data.getvalue())
          bucketName = body.get("bucketName")

      except Exception as e:
          error = 'Input a JSON object in the format: \'{"bucketName": "<bucket name>"}\' '
          return response.Response(
          ctx, response_data=json.dumps(
              {"error": error}),
          headers={"Content-Type": "application/json"}
          )
      resp = do(provider, bucketName)

      return response.Response(
          ctx, response_data=json.dumps(resp),
          headers={"Content-Type": "application/json"}
      )
  ```

  Do method
  Create the following method.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```python
  def do(provider, bucketName):
  ```
  This is where we'll put the bulk of our code that will connect to OCI and return the list of objects in the passed in bucket

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```python
      client = oci.object_storage.ObjectStorageClient(provider.config, signer=provider.signer)

      try:
          print("Searching for objects in bucket " + bucketName, file=sys.stderr)
          object = client.list_objects(os.environ.get("OCI_NAMESPACE"), bucketName)
          print("found objects", file=sys.stderr)
          objects = [b.name for b in object.data.objects]
          print(object.data, file=sys.stderr)
      except Exception as e:
          objects = str(e)

      response = {
          "The objects found in bucket '" + bucketName + "'": objects,
      }
      return response
  ```
  Here we are creating an [ObjectStorageClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/client/oci.object_storage.ObjectStorageClient.html) from the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html), which allows us to connect to OCI with the provider's data we get from our Mock Resource Principals and it allows us to make a call to gain access to object storage services.

## Put Objects
Handler method
 This is what is called when the function is invoked by Oracle Functions, delete what is given from the boilerplate and update it to contain the following:

 ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
 ```python
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
 ```

 Do method
 Create the following method.

 ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
 ```python
def do(provider, bucketName, fileName, content):
 ```
 This is where we'll put the bulk of our code that will connect to OCI and put our object into the bucket provided.

 ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
 ```python
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
 ```
 Here we are creating an [ObjectStorageClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/client/oci.object_storage.ObjectStorageClient.html) from the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html), which allows us to connect to OCI with the provider's data we get from our Mock Resource Principals and it allows us to make a call to gain access to object storage services.

Test
----
### Deploy the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  fn -v deploy --app <your app name> --all
  ```

  e.g.

  ```
  fn -v deploy --app python-object-storage --all
  ```

### Invoke the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAU543BZGF6V5TKHRH25CUILE)
  ```
  echo -n <JSON object> | fn invoke <your app name> <your function name>
  ```
  e.g.
  ```
  echo -n '{"fileName": "<file-name>", "bucketName": "<bucket-name>"}' | fn invoke python-object-storage list-objects
  echo -n '{"fileName": "<file-name>", "bucketName": "<bucket-name>", "content": "<content>"}' | fn invoke python-object-storage put-objects
  ```
  Upon success, you should see either a list of objects or a success message appear in your terminal.

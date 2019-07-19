# Using Resource Principals to Access Object Storage with the OCI Python SDK

  This function uses the OCI Python SDK to create a Resource Principals Signer to authenticate a function call to OCI's Object Storage.

  Uses the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html) to create a client that gets access to OCI Object Storage.

  In this example we'll show how you can access your OCI Object Storage information from a function using your tenancy's Object Storage Namespace, a bucket's name, a file's name, and JSON objects! To do this we'll use one API client exposed by the OCI SDK:

  1. [ObjectStorageClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/client/oci.object_storage.ObjectStorageClient.html) which allows us to connect to OCI with the use of [Resource Principals](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/signing.html?highlight=Resource%20Principals#resource-principals-signer) which authenticates our call to Object storage services.

  As you make your way through this tutorial, look out for this icon. ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE) Whenever you see it, it's time for you to perform an action.


Pre-requisites:
---------------
  1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

  2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

  3. Have your Oracle Object Storage Namespace available. This can be found by logging into your [cloud account](https://console.us-ashburn-1.oraclecloud.com/), and navigating to your Tenancy information.

### Switch to the correct context
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  fn use context <your context name>
  ```
  Check using
  ```
  fn ls apps
  ```

### Create or Update your Dynamic Groups
  In order to use and retrieve information about other OCI Services you must grant access to your Function via a dynamic group. For information on how to create a dynamic group, click [here.](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To)

  When specifying a rule, consider the following examples:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
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

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  Allow dynamic-group <your dynamic group name> to inspect object-family in compartment <your compartment name>
  ```
  e.g.
  ```
  Allow dynamic-group demo-func-dyn-group to inspect object-family in compartment demo-func-compartment
  ```

  For more information on how to create policies, go [here.](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm)


Create Applications
--------------------
1. Create an Application that is connected to Oracle Functions

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]
  ```

  You can find the subnet-ocid by logging on to [cloud.oracle.com](https://cloud.oracle.com/en_US/sign-in), navigating to Core Infrastructure > Networking > Virtual Cloud Networks. Make sure you are in the correct Region and Compartment, click on your VNC and select the subnet you wish to use.

  e.g.
  ```
  fn create app python-object-storage --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]'
  ```

  2. Clone this repository in a separate directory

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-control-instances/master/images/userinput.png?token=AK4AYAQ534QXEF2JHIDUZRS5BP632)
  ```
  git clone https://github.com/arodri202/oci-python-object-storage.git
  ```
  3. Change to the correct directory where you cloned this example.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-control-instances/master/images/userinput.png?token=AK4AYAQ534QXEF2JHIDUZRS5BP632)
  ```
  cd oci-python-object-storage
  ```
  4. Enter each function's directory and update the `func.yaml` to include the desired tenancy's Object Storage Namespace

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-control-instances/master/images/userinput.png?token=AK4AYAQ534QXEF2JHIDUZRS5BP632)
  ```
  config:
    OCI_NAMESPACE: <TO BE FILLED>
  ```

Test
----
### Deploy the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  fn -v deploy --app <your app name> --all
  ```
  > Note: If you wish to use repo as your application, change the app name in the `app.yaml` to reflect the desired name of your application

  e.g.

  ```
  fn -v deploy --app python-object-storage --all
  ```

### Invoke the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  echo -n <JSON object> | fn invoke <your app name> <your function name>
  ```
  e.g.
  ```
  echo -n '{"fileName": "<file-name>", "bucketName": "<bucket-name>"}' | fn invoke python-object-storage get-object
  echo -n '{"fileName": "<file-name>", "bucketName": "<bucket-name>", "content": "<content>"}' | fn invoke python-object-storage put-object
  echo -n '{"bucketName": "<bucket-name>"}' | fn invoke python-object-storage list-object
  ```
  Upon success, you should see either a list of objects or a success message appear in your terminal.

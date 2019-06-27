import base64
import json
import os.path
import sys

from fdk import response

import oci.auth.signers.security_token_signer
import oci.signer


class ResourcePrincipalProvider:
    def __init__(self):
        self.reload()

        # Pull our tenancy from the RPST
        claims = json.loads(b64(self.rpst.split(".")[1]))
        self.tenancy = claims["res_tenant"]
        self.compartment = claims["res_compartment"]
        self.fn_id = claims["sub"]

        self.config = {"region": os.environ["OCI_REGION"], "tenancy": self.tenancy}

    def reload(self):
        base_dir = os.environ["OCI_RESOURCE_PRINCIPAL_DIR"]

        with open(os.path.join(base_dir, "rpst")) as f:
            self.rpst = f.read().strip()

        self.private = oci.signer.load_private_key_from_file(os.path.join(base_dir, "private.pem"))
        self.signer = oci.auth.signers.security_token_signer.SecurityTokenSigner(self.rpst, self.private)


def b64(s):
    s += "=" * ((4 - len(s) % 4) % 4)
    try:
        return base64.b64decode(s)
    except:
        pass
    if s.startswith("ST$"):
        try:
            return base64.b64decode(s[3:])
        except:
            pass
    return s


class MockResourcePrincipalProvider:
    """Something that looks like a ResourcePrincipalProvider but just uses the user's (developer's) local files in the deployment"""

    def __init__(self, profile=None, config_file="~/.oci/config"):
        if profile is None:
            profile = os.environ.get("OCI_CLI_PROFILE", "DEFAULT")

        self.tenancy = self.get_env_var("OCI_TENANCY")
        self.compartment = os.environ.get("OCI_COMPARTMENT", self.tenancy)
        self.region = self.get_env_var("OCI_REGION")
        self.config = self.create_config()

        self.signer = oci.signer.Signer(
            tenancy=self.tenancy,
            user=self.config['user'],
            fingerprint=self.config['fingerprint'],
            pass_phrase=self.config['pass_phrase'],
            private_key_content=b64(self.get_env_var("OCI_PRIVATE_KEY_BASE64")),
            private_key_file_location=self.config['key_file'],
            )

    def get_env_var(self, key):
        val = os.environ.get(key)
        if not val:
            raise Exception(f"{key} is not set")

        return val

    def create_config(self):
        config = {
            "user": self.get_env_var("OCI_USER"),
            "compartment": self.compartment,
            "fingerprint": self.get_env_var("OCI_FINGERPRINT"),
            "tenancy": self.tenancy,
            "pass_phrase": os.environ.get("OCI_PRIVATE_KEY_PASS", ""),
            "region": self.region,
            "key_file": None,
        }
        oci.config.validate_config(config)
        return config

    def reload(self):
        pass

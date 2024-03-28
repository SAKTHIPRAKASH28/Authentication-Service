from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def load_rsa_keys():
    with open('./certs/private_key.pem', 'rb') as private_key_file:
        private_key_data = private_key_file.read()
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
            backend=default_backend()
        )

    with open('./certs/public_key.pem', 'rb') as public_key_file:
        public_key_data = public_key_file.read()
        public_key = serialization.load_pem_public_key(
            public_key_data,
            backend=default_backend()
        )

    return private_key, public_key


private_key, public_key = load_rsa_keys()

import os
import random

from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def gen_rsa(directory):
    key = rsa.generate_private_key(backend=crypto_default_backend(), public_exponent=65537, key_size=2048)
    private_key = key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH)

    if directory is not None:
        with open(os.path.join(directory, 'id_rsa'), 'wb') as private:
            private.write(private_key)

        with open(os.path.join(directory, 'id_rsa.pub'), 'wb') as public:
            public.write(public_key)


def gen_key():
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])


def generate():
    print("Generating secrets")
    print("Generating RSA keys")
    key_directory = os.path.join(os.getcwd(), "keys")
    if not os.path.exists(key_directory):
        os.mkdir(key_directory)
    gen_rsa(key_directory)

    print("Done")


if __name__ == '__main__':
    generate()
import os
import random

from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

TEMPLATE = """
#!/bin/bash
export SECRET_KEY='{key}'
export SECRET_KEY_PRIVATE=`cat {keypath}/id_rsa`
export SECRET_KEY_PUBLIC=`cat {keypath}/id_rsa.pub`
export ALLOWED_HOSTS='["localhost"]'
export PRODUCTION='1'
"""


def gen_ssh(dir):
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    with open(os.path.join(dir, 'id_rsa'), 'wb') as private:
        private.write(private_key)

    with open(os.path.join(dir, 'id_rsa.pub'), 'wb') as public:
        public.write(public_key)


def gen_key():
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])


def generate():
    with open("secrets2.sh", "w") as file:
        directory = os.path.join(os.getcwd(), "keys")
        if not os.path.exists(directory):
            os.mkdir(directory)
        gen_ssh(directory)
        file.write(TEMPLATE.format(key=gen_key(), dbname="dbname", dbuser="dbuser", dbpass="dbpass", keypath=directory))


if __name__ == '__main__':
    generate()

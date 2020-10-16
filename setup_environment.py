#!/usr/bin/env python3
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

STARTUP_SCRIPT_TEMPLATE = """\
#!/bin/bash
export PRODUCTION='0'
export SECRET_KEY="{key}"
export ALLOWED_HOSTS='["localhost"]'


export RSA_PUB='{rsa_pub}'
export RSA_PRIV="{rsa_priv}"

"""

STARTUP_ENV_TEMPLATE = STARTUP_SCRIPT_TEMPLATE.replace("export ", "").replace("#!/bin/bash", "")

DJANGO_SECRET_KEY_SIZE = 50
RSA_KEY_SIZE = 2048
RSA_PUB_EXPONENT = 65537
CHAR_RANGE = (string.ascii_letters + string.punctuation).replace('"', "")


def gen_key():
    return "".join(random.choices(CHAR_RANGE, k=DJANGO_SECRET_KEY_SIZE))


def gen_rsa():
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=RSA_PUB_EXPONENT, key_size=RSA_KEY_SIZE)

    pub = key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
    priv = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())

    return pub.decode('utf-8'), priv.decode('utf-8')


if __name__ == '__main__':
    django_key = gen_key()
    rsa_pub, rsa_priv = gen_rsa()

    with open(".env", "w") as f:
        f.write(STARTUP_ENV_TEMPLATE.format(key=django_key, rsa_pub=rsa_pub, rsa_priv=rsa_priv))

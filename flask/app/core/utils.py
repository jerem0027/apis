#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

import bcrypt


# Generateur de mot de passe basic
def generate_password(length=16) -> None:
    characters = string.ascii_letters + string.digits +  string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print("Mot de passe généré :", password)

# password = generate_password()


def encode_pass(passw:str) -> bytes:
    return bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())

def decode_pass(passwd:str, pass_hached:str) -> bool:
    return bcrypt.checkpw(passwd.encode('utf-8'), pass_hached)
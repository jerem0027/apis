#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

from passlib.hash import bcrypt


def random_number(size):
    lst_rand = []
    for _ in range(0,1000):
        lst_rand.append(random.randint(0,size-1))

    return lst_rand[random.randint(0,len(lst_rand)-1)]


# Generateur de mot de passe basic
def generate_password(length=16) -> None:
    characters = string.ascii_letters + string.digits +  string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print("Mot de passe généré :", password)

# password = generate_password()


def encode_pass(passw:str) -> bytes:
    return bcrypt.using(rounds=15).hash(passw).encode('utf-8')

def decode_pass(passwd:str, pass_hached:str) -> bool:
    return bcrypt.verify(passwd, pass_hached)
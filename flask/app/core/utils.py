#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string

os.environ["export PYTHONIOENCODING"] = "UTF-8"

def random_number(size):
    lst_rand = []
    for i in range(0,1000):
        lst_rand.append(random.randint(0,size-1))

    return lst_rand[random.randint(0,len(lst_rand)-1)]


# Generateur de mot de passe basic
def generate_password(length=16) -> None:
    characters = string.ascii_letters + string.digits +  string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print("Mot de passe généré :", password)

# password = generate_password()
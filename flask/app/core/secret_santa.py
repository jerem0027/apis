#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from copy import copy
from uuid import uuid4


def random_number(size):
    if size == 0:
        size +=1
    return random.randint(0, size-1)

def create_associations(guests:list) -> list:
    for guest in guests:
        guest["link"] = str(uuid4())

    ended = False
    while not ended:
        guest_done = []
        target_tmp = copy(guests)

        for guest in guests:
            target = target_tmp[random_number(len(target_tmp))]
            if target in guest_done:
                break
            if target != guest:
                guest["target_link"] = target["link"]
                guest_done.append(target)
                target_tmp.remove(target)
        ended = len(target_tmp) == 0
    return guests
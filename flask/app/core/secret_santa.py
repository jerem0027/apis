#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from copy import copy


def random_number(size):
    if size == 0:
        size +=1
    return random.randint(0, size-1)

def create_associations(guests:list) -> list:
    ended = False
    while not ended:
        guest_done = []
        target_tmp = copy(guests)

        for guest in guests:
            target = target_tmp[random_number(len(target_tmp))]
            if target in guest_done:
                break
            if target != guest:
                guest["target"] = target["name"]
                guest["target_email"] = target["email"]
                guest_done.append(target)
                target_tmp.remove(target)
        ended = len(target_tmp) == 0
    return guests
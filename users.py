#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
The task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map returns a set of unique user IDs ("uid")
"""

def get_user(element):

    uid = element.get('uid')
    return uid


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        uid = get_user(element)
        if uid:
            users.add(uid)
        else:
            pass
    return users


def test():

    users = process_map('sample.osm')
    pprint.pprint(len(users))


if __name__ == "__main__":
    test()

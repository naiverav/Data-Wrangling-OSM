#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The count_tags function returns a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.

"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tag_dict = {}

    for event, element in ET.iterparse(filename):
        if element.tag not in tag_dict.keys():
            tag_dict[element.tag] = 1
        else:
            tag_dict[element.tag] += 1
    return tag_dict


def test():

    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    
if __name__ == "__main__":
    test()

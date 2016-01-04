#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
import audit as project_audit
import data as project_data
from collections import defaultdict

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# Get a sample from the full OSM file by writing one of every 20 elements
def get_sample(input_file, output_file):
    with open(output_file, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every 20th top level element
        for i, element in enumerate(get_element(input_file)):
            if i % 20 == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>')

# Audit the OSM file.
# This function returns:
#    - a dictionary of street names keyed by street type, and
#    - a dictionary of counts keyed by street type
def audit2(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if project_audit.is_street_name(tag):
                    project_audit.audit_street_type(street_types, tag.attrib['v'])

    type_count = {}
    for s in street_types:
        if s not in type_count:
            type_count[s] = 0
        type_count[s] = len(street_types[s])

    return street_types, type_count

# Convert the input OSM file to JSON file.
# The process will replace abbreviated street types to full name.
# For example, 'Taikoo Shing Rd' -> 'Taikoo Shing Road'
def convert_map(input_file):
    project_data.process_map(input_file, True)

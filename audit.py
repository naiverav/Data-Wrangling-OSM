"""
The task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    The mappings are only for the actual problems we find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

####Audit Street Names
mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "blvd": "Boulevard",
            "Cir": "Circle",
            "Ct": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "DRIVE": "Drive",
            "E": "East",
            "FM": "Farm-to-Market Road",
            "Fm": "Farm-to-Market Road",
            "Frwy": "Freeway",
            "Fwy": "Freeway",
            "Hwy": "Highway",
            "HIGHWAY": "Highway",
            "Ln": "Lane",
            "N": "North",
            "N,": "North",
            "Pkwy": "Parkway",
            "Pkwy,": "Parkway",
            "Pwky": "Parkway",
            "Pky": "Parkway",
            "Plaze": "Plaza",
            "Rd.": "Road",
            "Rd": "Road",
            "S": "South",
            "S.": "South",
            "St.": "Street",
            "St": "Street",
            "ST": "Street",
            "Ste": "Suite", 
            "Stree": "Street",
            "street": "Street",
            "Trl": "Trail",
            "W.": "West",
            "W": "West",
            "Westhimer": "Westheimer"
          }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


#This function accepts the name and mapping as parameters and returns the updated name
#We iterate over each word of the street name and keep updating each one if found in mapping except if the street is an Avenue.
def update_streetname(name, mapping):
    parts = name.split()
    for i in range(len(parts)):
        if parts[i] in mapping.keys():
            #checking if the street is not an Avenue, in which case, it remains as such eg. Avenue S, do not convert to Avenue South
            if parts[0] != "Avenue":
                parts[i] = mapping[parts[i]] 
                name = " ".join(parts)
    return name


def test_streetname():
    st_types = audit('OSMFILE')
    pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_streetname(name, mapping)
            print name, "=>", better_name






         
####Audit PostCode


postcode_re = re.compile(r'^(\d{5}$)')

def audit_postcode_err(bad_postcodes, postcode):
    p = postcode_re.search(postcode)
    if p == None:
        bad_postcodes[postcode].add(postcode)


def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    bad_postcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    audit_postcode_err(bad_postcodes, tag.attrib['v'])
    osm_file.close()
    return bad_postcodes


#Compiling the bad postcode formats 
d5_d4 = re.compile(r'^(7\d{4})-\d{4}$') #find 5 digit pattern in (5 digits) hyphen 4 digits

str_d5 = re.compile(r'^[a-zA-Z]{2}\s(\d{5})$') #two alphabets space (5 digit) 

d5_chr  = re.compile(r'^(\d{5}).+$') #(5 digits) followed by more numbers or alphabets in continuation


#This function takes the bad postcode as an argument and returns the updated postcode
def update_postcode(postcode):
    if re.match(d5_d4, postcode):
        correct_postcode = re.findall(d5_d4,postcode)[0]
    elif re.match(str_d5, postcode):
        correct_postcode = re.findall(str_d5,postcode)[0]
    elif re.match(d5_chr, postcode):
        correct_postcode = re.findall(d5_chr, postcode)[0]
    else:
        return postcode
    return correct_postcode

  
def test_postcode():
    postcodes = audit_postcode(OSMFILE)
    
    for p_code, ways in postcodes.iteritems():
        for code in ways:
            correct_postcode = update_postcode(code)
            print code, "=>", correct_postcode



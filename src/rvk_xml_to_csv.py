"""
Python script to transform an xml file  given by the library classification
Regensburger Verbundklassifikation (RVK) to an csv file. The csv file only contains
the call number (notation) and the name (benennung).
"""

import os
import xml.etree.ElementTree as ET
import csv

from configuration import PROJECT_ROOT

DIR_PATH = 'data/helper_files'
# current xml RVK-XML-FILE 
# see: https://rvk.uni-regensburg.de/regensburger-verbundklassifikation-online/rvk-download
XML_FILE ='rvko_2020_3.xml'
CSV_FILE = 'rvk_data.csv'

XML_FILE_PATH = os.path.join(PROJECT_ROOT, DIR_PATH, XML_FILE)
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, DIR_PATH, CSV_FILE)

def read_xml_file(xml_file):

    """Parsing the xml-file from the Regenburger Verbundklassifikation (RVK) using
    the module xml.etree.ElementTree


    Returns
    -------
    my_list
        returns an array of dictionaries
    """


    # checking if file exists
    if not os.path.exists(XML_FILE_PATH):
        print('The file does not exists.')

    # parsing the xml file
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()

    # creating a list with the specific attributes
    # my_list = [notation.attrib for notation in root.iter('node')]
    my_list = [children.attrib for children in root.iter('node')]

    return my_list

def transform_to_csv(my_list):

    """Transform the given list of dictionaries into an csv-file

    """
    # creating an csv file
    csv_file = os.path.abspath(CSV_FILE_PATH)

    # checking if file exists
    if os.path.exists(csv_file):
        print('The file does exists.')


    # creating fieldnames for the csv file
    csv_col = ['notation', 'benennung']


    # open and write the data into the csv-file
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_col)
        writer.writeheader()
        for data in my_list:
            writer.writerow(data)


def main():
    """Calling the other functions with the xml file
    """
    # path to your file
    xml_file = XML_FILE_PATH
    result = read_xml_file(xml_file)
    if result:
        transform_to_csv(result)


if __name__ == "__main__":
    main()

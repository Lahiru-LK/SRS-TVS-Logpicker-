import argparse
import os
import shutil
import xml.etree.ElementTree as ET
import logging
import tarfile
import base64
import re
from datetime import datetime

# Global variable for the temporary extraction directory
temporary_extraction_directory = "temp_extraction"

def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define default namespace
        ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

        # Extract timestamp from XML using default namespace
        timestamp_element = root.find(".//ss:Worksheet/ss:Table/ss:Row/ss:Cell[@ss:StyleID='A']/ss:Data[@ss:Type='String']", namespaces=ns)

        if timestamp_element is not None and timestamp_element.text is not None:
            timestamp_str = timestamp_element.text.strip()  # Keep timestamp as string without modification
            return timestamp_str
        else:
            print("Error: Timestamp element not found or text is None in the XML.")
            print(f"XML structure:\n{ET.tostring(root, encoding='utf-8').decode('utf-8')}")
            exit(1)
    except Exception as e:
        print(f"Error parsing XML: {str(e)}")
        exit(1)



def encode_binary_data(xml_content):
    # Use regular expression to find binary data inside Data elements
    pattern = r"<Data ss:Type='String'>\[(.*?)\]</Data>"
    matches = re.findall(pattern, xml_content, re.DOTALL)

    # Encode binary data as base64
    for match in matches:
        encoded_data = base64.b64encode(match.encode()).decode()
        xml_content = xml_content.replace(f"<Data ss:Type='String'>[{match}]</Data>", f"<Data ss:Type='String'>{encoded_data}</Data>")

    return xml_content

# Read XML file content with explicit encoding
with open("F:\\GALLERY\\Fiverr\\Order Project\\python\\01\\temp_extraction\\TVSlog_202006226_10104214\\TestScenario.xml", "r", encoding="utf-8") as xml_file:

    xml_content = xml_file.read()

# Encode binary data and replace in the XML content
encoded_xml_content = encode_binary_data(xml_content)

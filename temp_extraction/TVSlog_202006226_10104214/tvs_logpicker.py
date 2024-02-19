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



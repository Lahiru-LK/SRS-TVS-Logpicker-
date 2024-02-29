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




def check_log_entries(log_file_path, log_entries, display=False):
    try:
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()

            # Handle the case where log_entries is empty
            if not log_entries:
                print(f"Warning: Log entries list is empty for {log_file_path}. Skipping entry check.")
                return False

            for entry in log_entries:
                if entry in log_content:
                    return True
    except Exception as e:
        print(f"Error checking log entries in {log_file_path}: {str(e)}")
        return False

    return False


def extract_files_from_archive(archive_path):
    extracted_files = []

    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Extract the contents of the archive
            tar.extractall(path=temporary_extraction_directory)
            extracted_files = [os.path.join(temporary_extraction_directory, extracted_file) for extracted_file in os.listdir(temporary_extraction_directory)]
    except tarfile.ReadError:
        print(f"Error: {archive_path} is not a valid gzip-compressed tar archive.")
    except Exception as e:
        print(f"Error extracting files from archive {archive_path}: {str(e)}")

    return extracted_files

def find_matching_archive(logroot, expected_timestamp):
    matching_logs = []

    # Iterate through archives in the root directory
    for file in os.listdir(logroot):
        log_file_path = os.path.join(logroot, file)

        # Check if the file is a tar.gz archive
        if file.endswith(".tar.gz"):
            extracted_files = extract_files_from_archive(log_file_path)
            # Check each extracted file for relevant log entries
            for extracted_file_path in extracted_files:
                if check_log_entries(extracted_file_path, expected_timestamp):
                    display_log_file(extracted_file_path)
                    matching_logs.append((log_file_path, extracted_file_path))

    if not matching_logs:
        # No match found in the root directory
        print("Error: No matching archive found for the given timestamp.")

    return matching_logs

def display_log_files(output_directory, expected_timestamp):
    log_files = []

    # Find all .log files in the output directory
    for root, dirs, files in os.walk(output_directory):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))

    if log_files:
        print(f"\nLog files in the directory: {output_directory}\n")
        for log_file in log_files:
            print(f"{log_file}\n")
    else:
        print("No log files found in the directory.")


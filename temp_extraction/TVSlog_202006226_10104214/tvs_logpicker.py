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


def display_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as log_file:
            print(log_file.read())
    except Exception as e:
        print(f"Error displaying content of log file: {str(e)}")

def display_jru_files(output_directory, expected_timestamp):
    jru_files = []

    # Find all .jru files in the output directory
    for root, dirs, files in os.walk(output_directory):
        for file in files:
            if file.endswith(".jru"):
                jru_files.append(os.path.join(root, file))

    if jru_files:
        print(f"\nJRU files in the directory: {output_directory}\n")
        for jru_file in jru_files:
            print(f"{jru_file}\n")
    else:
        print("No JRU files found in the directory.")




        def main():
        print("\n")
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Logfile picker for TestScenario.xml and log archives")
    parser.add_argument("-v", "--version", action="version", version="tvs_logpicker 1.2")
    parser.add_argument("-f", "--filename", required=True, help="Path to TestScenario.xml file")
    parser.add_argument("-l", "--logroot", default=os.getcwd(), help="Root path for log archives")
    parser.add_argument("-o", "--output", default=os.path.join(os.getcwd(), "output"), help="Output directory")
    parser.add_argument("-d", "--display-entry", dest="display_entry", help="Display specific log entry content")

    # Handle argument parsing errors
    args = parser.parse_args()

    # Ensure output and temporary extraction directories exist
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(temporary_extraction_directory, exist_ok=True)

    # Parse XML and find matching archive
    try:
        timestamp_str = parse_xml(args.filename)
        expected_timestamp = timestamp_str  # Use timestamp as string without modification
        matching_archive = find_matching_archive(args.logroot, expected_timestamp)
    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        return

    if matching_archive:
        # Copy files to output directory
        try:
            shutil.copy(args.filename, args.output)
            for log_archive, extracted_log in matching_archive:
                if log_archive:
                    shutil.copy(log_archive, args.output)  # Copy the tar.gz archive
                if extracted_log:
                    shutil.copy(extracted_log, args.output)  # Copy the extracted file if available
        except Exception as e:
            logging.error(f"Error copying files: {str(e)}")

        # Display the specific log entry content if specified
        if args.display_entry:
            log_entries_to_check = [args.display_entry]
            for root, dirs, files in os.walk(args.output):
                for file in files:
                    file_path = os.path.join(root, file)

                    # Check if the file is a log or jru file
                    if file.endswith(".log"):
                        logging.info(f"\nChecking log file: {file_path}")
                        check_log_entries(file_path, log_entries_to_check)
                    elif file.endswith(".jru"):
                        logging.info(f"\nChecking JRU file: {file_path}")
                        display_log_file(file_path)

        # Remove the temporary extraction directory
        shutil.rmtree(temporary_extraction_directory)

if __name__ == "__main__":
    main()
    print("\n")

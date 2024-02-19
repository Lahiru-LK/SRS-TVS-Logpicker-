# SRS TVS Logpicker 🕵️‍♂️📆

![py](https://github.com/Lahiru-LK/SRS-TVS-Logpicker-/assets/104630433/3cba3a09-b88f-4767-8d71-eabdae87b61b)

## Overall Description 🌐

During work in the simulation lab, system crashes can occur. To simplify the process of sending the TestScenario.xml file and corresponding logfile archive to the support team, the "tvs_logpicker" script is introduced. This standalone Python3 application automates the manual searching and matching of TestScenario files and archive files, making the process more convenient.

## Functional Requirements 🛠️

### CLI Commands

- **FR-CLI-1:** Output of app version
  ```bash
  $ python3 tvs_logpicker.py --version 🚀
  ```

- **FR-CLI-2:** Output of app help
  ```bash
  $ python3 tvs_logpicker.py --help ❓
  ```

- **FR-CLI-3:** Definition of input path to the TestScenario.yml file name as an argument
  ```bash
  $ python3 tvs_logpicker.py -f TestScenario.xml 📂
  ```

- **FR-CLI-4:** Definition of root path for log archives
  ```bash
  $ python3 tvs_logpicker.py -f TestScenario.xml -l /home/pluto/Desktop/ 📦
  ```

### Processing

- **FR-Processing-1:** Parse the search parameters from the file TestScenario.xml
- **FR-Processing-2:** Find log archives that match the search criteria

### Output

- **FR-Output-1:** Copy pairs (TestScenario.xml and LogArchive) to an output directory
  ```bash
  $ python3 tvs_logpicker.py -f TestScenario.xml -l /home/pluto/Desktop/ -o outdir 📂
  ```

- **FR-Output-2:** Log messages for the user 📝
- **FR-Output-3:** Error handling / Error Messages ❌

## Match Criterion 🔍

To find the right archive, an equal value of the timestamp variable must be taken and compared. If the timestamp of the two files is equal, the TestScenario.xml file and the full archive must be copied to the output directory. If the timestamp does not match, use the same timestamp for the next possible logfile file inside the current archive.

### Timestamp TestScenario.xml 📅

The relevant attributes from the subelement row inside the train element are:

- **Timestamp:** Text of the 0 Cell Element (e.g., 10:33:47.036 or 10:20:40.685)
- **LogEntry:** Text of the 3 Cell Element (e.g., Activate=1 282_test.log TYPE=930 NAME=LOGGING.activate)

### Timestamp LogArchive 🗂️

The timestamp is found inside one of the following archived subfiles `.log_obu*`.

## Non-Functional Requirements 🧰

- **NFR-1:** Environment - CLI Python App for Linux (Ubuntu) and Windows 10 ✔️
- **NFR-2:** In Code Documentation 📚

# This file is licensed under the GNU General Public License v3.0


import hl7
import os
import datetime
import configparser
import threading
from pathlib import Path


config = configparser.ConfigParser()
config.read('config/testing.ini')


# Configure the test process from the config file from above
logfile         = config['Setup']['logfile']
input_folder    = config['Setup']['input_folder']
output_folder   = config['Setup']['output_folder']
write_output    = config['Setup']['write_output']


def test_all_to_hl7(log, hl7, filename):
    """Tests the result of rebuilding the HL7 from all formats.

    As the different formats are already generated on creating the message
    object, only the conversion back to list and then HL7 are needed.

    Args:
        log (object): current open log file 
        hl7 (object): HL7 object 
        filename (string): File name/path for desired HL7
    """
    original = hl7.hl7_message

    hl7.list_to_hl7()
    compare(log, 'List to HL7', filename, hl7.hl7_message, original)

    hl7.dict_to_list()
    hl7.list_to_hl7()
    compare(log, 'Dict to HL7', filename, hl7.hl7_message, original)

    hl7.json_to_list()
    hl7.list_to_hl7()
    compare(log, 'JSON to HL7', filename, hl7.hl7_message, original)


def compare(log, test, filename, result, original):
    """Compares the given result to the given original and logs the result

    Args:
        log (Object): The open log text file
        test (string): The name of the test
        filename (string): The name of the text file
        result (any): result of a transformation
        original (string): original state of data before transformation
    """
    global passed
    global failed

    if result != original:
        failed += 1
        log_result(log, test, False, filename)
        log.write(f"{filename}\n\n{original}\n\n{result}\n\n")
    else:
        passed += 1
        log_result(log, test, True, filename)
    

def log_result(log, test_type, result, filename):
    """Logs the result of a test to the file object with the current date and time

    Args:
        log (Object): The open log text file
        test_type (string): The name of the test
        filename (string): The name of the text file
        result (any): result of a transformation
    """
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"[{current_time}][{test_type}] {filename}: {'Passed' if result else 'Failed'}\n")


def process_file(log, filename):
    """Executes testing for a text file. 

    Args:
        log (Object): The open log text file
        filename (string): The name of the text file
    """
    with open(f"{input_folder}/{filename}", "r") as file:
        message = file.read()
        hl7_message = hl7.HL7(message)

        basename = os.path.splitext(os.path.basename(filename))[0]

        if write_output:
            Path(f'{output_folder}/hl7_to_list').mkdir(parents=False, exist_ok=True)
            Path(f'{output_folder}/hl7_to_dict').mkdir(parents=False, exist_ok=True)
            Path(f'{output_folder}/hl7_to_json').mkdir(parents=False, exist_ok=True)
            Path(f'{output_folder}/hl7_to_excel').mkdir(parents=False, exist_ok=True)
            Path(f'{output_folder}/hl7_structure').mkdir(parents=False, exist_ok=True)

            hl7_message.export('list', f'{output_folder}/hl7_to_list/{basename}_list')
            hl7_message.export('dict', f'{output_folder}/hl7_to_dict/{basename}_dict')
            hl7_message.export('structure', f'{output_folder}/hl7_structure/{basename}_structure')
            hl7_message.export('json', f'{output_folder}/hl7_to_json/{basename}')
            hl7_message.export('excel', f'{output_folder}/hl7_to_excel/{basename}')

        test_all_to_hl7(log, hl7_message, filename)


def main():
    global passed
    global failed

    passed = 0
    failed = 0

    with open(logfile, 'w') as log:
        threads = []
        for file in os.listdir(f'{input_folder}'):
            print(file)
            thread = threading.Thread(target=process_file, args=(log, file))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    print("====================")
    print(f"Passed: {passed} tests ")
    print(f"Failed: {failed} tests")
    print("====================")


if __name__ =='__main__':
    main()
    
    

    



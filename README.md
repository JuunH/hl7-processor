# hl7-processor

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Roadmap](#roadmap)
6. [License](#license)

## Introduction

HL7 Processor was created to help make reading and manipulating HL7 messages 
easier. 

It creates an object to model the HL7 message into different data structures to
offer varius options of working with it in other projects.

## Features
- Reading HL7 messages
- Conversion to an embedded list, dictionary, or JSON and reverse
- Display a formatted visual structure of the HL7 message
- Compare two HL7 messages
- Modification to any field using the Dictionary or JSON structure
- Export any structure to a text file
- Testing the conversion of multiple HL7 messages

## Installation

### Prerequisites
- openpyxl 3.1.2

### Setup
1. Clone the repository to anywhere in your project
    ```bash
    git clone https://github.com/username/repository-name.git
    ```

2. Move into the repository
    ```bash
    cd repository-name
    ```

3. Install the requirements for the project to run (in your own virtual environment).

    ```bash
    pip install -r requirements.txt
    ```

## Usage
Import the HL7 module into your project and using a HL7 stored from a txt file,
pass it as an argument into the class to create the object.

```Python
# May have to change location of module depending where its stored
import hl7 as h 

with open("path/to/hl7", "r") as file:
        message = file.read()
        hl7 = h.HL7(message)
```

Once created, the embedded list, dictionary, and JSON structures are generated
for you already.

```Python
# Example usage
print(hl7.elist)
print(hl7.structure)
print(hl7.hl7_message)
hl7.dict["MSH.5"]
hl7.json["MSH"][5]
hl7.export("excel", "random/location")
```


### Commands
List of commands for the HL7 class. Will assume an object is created under the
name hl7. 

The conversion commands does not return anything but instead modifies
the relevant structure attribute.

|Command|Description|Example Usage|
|-------|-----------|-------------|
|`hl7.hl7_to_list()`|Convert the raw HL7 to embedded list form|`hl7.hl7_to_list()`
|`hl7.list_to_hl7()`|Convert the embedded list back to raw HL7|`hl7.list_to_hl7()`
|`hl7.list_to_dict()`|Convert the embedded list to dictionary form|`hl7.list_to_dict()`
|`hl7.list_to_json()`|Convert the embedded list to JSON form|`hl7.list_to_json()`
|`hl7.dict_to_list()`|Convert the Dictionary form to embedded list form|`hl7.list_to_dict()`
|`hl7.json_to_list()`|Convert the JSON form to embedded list form|`hl7.json_to_list()`
|`hl7.structure()`|Return a formatted visual structure of the HL7 message|`hl7.json_to_list()`
|`hl7.export()`|Export a desired structure|`hl7.export('dict', 'path/to/save/filename`')

**Disclaimer**: If a change is made to the value of the dictionary form, it is not mirrored to the JSON or Embedded list form and vice versas. Ensure you map the changes or use the right structure when converting back to list and then raw HL7.

Extra function within the module but not the class. Helps compare two HL7 messages.
|Command|Description|Example Usage|
|-------|-----------|-------------|
|`compare()`|Compares the fields of two HL7 messages|`compare(original, result, filepath)`

### Testing
To test whether the HL7 module properly converts to and back to the raw HL7:

1.  Modify the `testing.ini` config file within the `config` folder to your requirements. 

    ```ini
    [Setup]
    input_folder = path/to/input
    output_folder = path/to/output
    write_output = False
    logfile = logs\current_log.txt
    ```

2. Run `hl7_test.py` on its own and review the output.

A log of the passed and failed tests to the given files will be recorded in
`logs/current_log.txt`. If `write_output` is set to `True`, it will create
individual folders (if not existing) for each structure in the output location
and store the relevant result in. 

## Roadmap

- Option for synced changes between forms
- GUI to interactive with the HL7


## License

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

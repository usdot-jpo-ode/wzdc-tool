# Work Zone Data Collection Toolset

## Project Description

This project is an open source, proof of concept work zone data collection tool. The purpose of this tool is to allow a construction manager in the field and transportation system manager at the Infrastructure Owner Operator (IOO) back-office  to map work zones and distribute generated map messages to third parties. This project is part of a larger effort on understanding mapping needs for V2X applications, funded by USDOT. This repository is a deliverable under the project and supports the Development and Demonstration of Proof-of-Concept of an Integrated Work Zone Mapping Toolset.

![Tasks 6-7 Diagram](./images/POC_WZ_Toolset.jpg)

This repository contains the following components:

- POC Work Zone Data Collection (WZDC) tool
- POC RSM(XML) to WZDx Translator
- Sample Files

Related repositories:
- [V2X Mobile Application](https://dev.azure.com/leidos-cav/WZDC-Tool/_git/AndroidApp)
- [V2X Website](https://dev.azure.com/leidos-cav/WZDC-Tool/_git/Website)
- [V2X Message Generation](https://dev.azure.com/leidos-cav/WZDC-Tool/_git/GenerateMessagesFunctionApp)

## Prerequisites

Requires:

- Python 3.6 (or higher)
  - azure-storage-blob
  - esptool
  - image
  - wheel
  - serial
  - requests
- Environment Variables (Optional, Contact Tony English at [tony@neaeraconsulting.com](mailto://tony@neaeraconsulting.com) for more information)

## Usage

The WZDC tool is a python-based tool that utilizes a user interface. Steps for starting and running the tool are listed below and are described in further detail here: [POC Toolset User Guide](./POC%20Toolset%20User%20Guide.pdf)

Video tutorials for each tool:
Website- Edit Work Zone - https://youtu.be/fBRkcWIBCWI
WZDC Mobile app - https://youtu.be/PMs6gDkm7NY
WZDC Computer app - https://youtu.be/pfD8pcYpGcE
Website - Config File - https://youtu.be/mm1Cm24tOIc


### Building

No building/compiling is required for this tool.

### Testing

There are currently no test cases for this proof of concept tool.

### Execution

#### Step 1: Run the WZDC script (from the Work Zone Data Collection Folder)

```
python WZDC_tool.py
```

#### Step 2: Load configuration file and confirm GPS connection

![Config Loading UI](./images/WZDC_tool_initialization_screen.jpg)
This component of the application enables a user to load a configuration file and verify their GPS connection. This configuration file can be loaded from the Cloud or from a local directory. A configuration file can be created at https://wzdctool.azurewebsites.net/V2X_ConfigCreator.
The tool automatically scans usb COM ports for a GPS device. The baudrate and data rate can be configured if needed
When a configuration file is loaded and a GPS connection is confirmed, data collection may begin

#### Step 3: Map work zone

![Data Colelction UI](./images/WZDC_tool_automatic_data_collection_screen.JPG)
This is the data collection component. Data collection begins when a set starting location is reached and ends when the ending location is reached (both set in configuration file). A user can mark lane closures and the presence of workers. The user interface shows the current state of the work zone, including the vehicle lane (set in configuration file). All of the data collected is saved in a CSV path data file, which will be used for message generation

![Data Colelction UI](./images/WZDC_tool_manual_data_collection_screen.JPG)
This is the Manual Detection mode of the data collection component. In this mode, data collection starts when the user presses the 'Mark Start of Work Zone' button. Data collection ends when the user presses the 'Mark End of Work Zone' button. These locations are saved as the automatic start/end locations for use the next time that work zone is mapped. 

#### Step 4: Upload generated messages to the cloud

![Upload UI](./images/upload_ui_screenshot.jpg)
After data collection is completed, message generation begins. The recorded path data (including lane closure/worker presence) is processed into an RSM (xml) message. This message is then converted into binary (UPER format). The xml message, along with some additional information included in the configuration file, is then converted into a WZDx message. These messages (and the CSV data file) are added to a ZIP archive. When the user has an internet conenction, they can initiate the upload to the cloud, where the messages are unzipped and organized. These messages are available to visualize, verify and publish on https://wzdctool.azurewebsites.net.

## Additional Notes

This toolset was developed as a proof of concept and is not able to provide a full solution for all types of work zones. Future work may expand the functionality of the tool to address more work zone types and add other features such as authentication or a mobile app version of the tool.

This tool functions alongside a POC TMC website (https://wzdctool.azurewebsites.net). Instructions for utilizing this website are located here: [POC Toolset User Guide](./POC%20Toolset%20User%20Guide.pdf)

Documentation for this project is located here: [Documentation](./Documentation). This documentation includes:

- V2X POC Interface Control Document
- V2X POC System Engineering Report
- V2X POC Test Case Results Report
- WZDC Tool Documentation Updates
  - Describes message generation

## Version History and Retention

**Status:** prototype

**Release Frequency:** This project is updated approximately once every 2 weeks

**Release History:** See [CHANGELOG.md](./CHANGELOG.md)

**Retention:** This project will remain publicly accessible for a minimum of five years (until at least 08/15/2025).

## License

This project is licensed under the CMIT License - see the [License.md](./LICENSE.md) for more details. 

### Guidelines

- Issues
  - Create issues using the SMART goals outline (Specific, Measurable, Actionable, Realistic and Time-Aware)
- PR (Pull Requests)
  - Create all pull requests from the master branch
  - Create small, narrowly focused PRs
  - Maintain a clean commit history so that they are easier to review

## Contact Information

Contact Name: Tony English
Contact Information: [tony@neaeraconsulting.com](mailto://tony@neaeraconsulting.com)

## Acknowledgements

To track how this government-funded code is used, we request that if you decide to build additional software using this code please acknowledge its Digital Object Identifier in your software's README/documentation.

Digital Object Identifier: https://doi.org/10.21949/1519288

## Abbreviations

CAMP tool: Crash Avoidance Metrics Partnership

POC: Proof of Concept

RSM: Roadside Safety Message

WZDC Tool: Work Zone Data Collection Tool

WZDx: Workzone Data Exchange


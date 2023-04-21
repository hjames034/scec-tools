# scec-tools
tools for SoCal Earthquake Center

There are two files that will help you in maintenance for the Great ShakeOut included here.

Prerequisites: 
1. Download this repository to your computer (visible on main GitHub page), download Python, modify the environment variables so you can modify it in terminal.
1a. Quick Guide for Installing Python
This is a quick guide for installing Python and modifying the environment variables to run it on Command Prompt.

Download the latest version of Python for your operating system from the official Python website at https://www.python.org/downloads/.

Run the installer and follow the prompts to install Python on your system.

Add the installation directory to the system's PATH environment variable to run Python from Command Prompt:

Open the Start menu and search for "Environment Variables".

Click on the "Edit the system environment variables" option.

In the System Properties window, click on the "Environment Variables" button.

Under "System Variables", scroll down and find the "Path" variable. Select it and click the "Edit" button.

In the Edit Environment Variable window, click the "New" button and enter the path to the directory where Python is installed (for example, "C:\Python39"). Click "OK" to close all the windows.

Close and reopen Command Prompt for the changes to take effect.

To verify that Python is installed correctly and can be run from the command line, type "python" and press Enter. This should launch the Python interpreter.
3. Install the required modules for running the SCEC scripts.

```pip install -r requirements.txt```

*Note: make sure all files that you need to use for the scripts are in the same directory*

## Fuzzy Search

```python fuzzysearch.py```

The fuzzySearch script finds records that are similar textually (i.e. Robb Elementary vs. Robb Elementary School), while considering parameters such as distance between the address of the records. The output is a table with all records that are potentially related. 

1. Export a selection of either: this year's records, or multiple year's records (for standardizing district names, I would recommend doing just this year's, but for standardizing org names, I would look at multiple years or records).
2. Select the following fields to be exported to a csv.

Businessname, category, primary_key,postalcode, event_key, tracker_key, PARTICIPANT_count, address1, address2, district

3. Move the file to the same directory (folder) as the fuzzysearch.py script.

4. Run the script in the command line with the following commands:

```python fuzzysearch.py INPUT_CSV_FILE OUTPUT_CSV_FILE FIELD(0-BUSINESSNAME,8-DISTRICT) GLOBAL_REGION(TRUE/FALSE)```


Example:
```python fuzzysearch.py fuzzydist_TZ_419.csv fuzzydistoutput_TZ_419.csv 8 True```

This example shows us finding the fuzzy matches from the fuzzydist_TZ_419.csv file and outputting it to fuzzydistoutput_TZ_419.csv. We are finding districts with similar names (hence the value of 8 for the third parameter). Putting the global region parameter as true will mean that we do not use a geographic filter as we do not have zipcode data for global regions. If we put it as false, we will be searching for geographic prxoimity in the fuzzy search as well. 

5. When the program is done running, open the output file in Excel (in the same folder). Remove the first line, and then Ctrl + A and Ctrl + T. This will create a table with the selection and make it easier to filter
6. See guide in ShakeOut Guide for rest of the procedure.

## Website Parsing (Broken Web Addresses)
```python exportedwebaddress.py```
1. Replace all web addresses with spaces with a blank field (i.e. https://Web Address -> blank field). You can do this by searching for =" " in Filemaker in the Web address field, and then deleting everything in a webaddress field, and then doing Ctrl + = to propogate the changes across all of the found records
2. Find all remaining web addresses for the year.
3. Export just the webaddress field
4. Run the script in the command line with the following commands: 

```python exportedwebaddress.py INPUT_CSV_FILE OUTPUT_CSV_FILE```


Example:
```python exportedwebaddress.py brokenwebaddress_UT_419.csv brokenwebaddress_UT_419.csv```

5. Go to the "failed_site_import" and import the websites.
6. Follow the instructions on the main document.
7. When done following the instructions on the main doc, delete those websties from the failed_site_import database(you can delete all websites!)

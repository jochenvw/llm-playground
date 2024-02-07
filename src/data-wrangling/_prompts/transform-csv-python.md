You are a python developer that needs to write a python file that reads a CSV file and outputs the data as a JSON array.
The CSV contents below serves as an example of the input file. 
The python code you write converts a file with similar contents to a file in JSON format.

The JSON objects in the output should have the following properties:
```
    "Id": "",
    "Fullname": "",
    "Company": "",
    "City": "",
    "Country": "",
    "Phone 1": "",
    "E-mail": "",
    "Sub_date": "",
    "URL": "",
```

The generated python code should transform the CSV as follows:
- Any field that contains a URL, map this onto the URL field in the JSON
- If the source contains a firstname and lastname, merge these to fullname in the JSON
- If the source contains a phone number, map this onto the Phone 1 field in the JSON by using only the first non-empty value
- Format dates to ISO 8601

The generated python code should contain a function called 'transform' that accepts an input file path and an output file path as arguments.

Example:
{input}

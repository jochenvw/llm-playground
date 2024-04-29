Parse the following CSV file and parse the full contents to JSONL format.

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

The response must meet the following requirements:
- Any field that contains a URL, map this onto the URL field in the JSON
- If the source contains a firstname and lastname, merge these to fullname in the JSON
- If the source contains a phone number, map this onto the Phone 1 field in the JSON by using only the first non-empty value
- Format dates to ISO 8601


Input:
{input}

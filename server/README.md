# Data Anonymization Tool (API)
This is a Flask-based server that provides APIs for anonymizing sensitive data in CSV files and text. It utilizes various techniques such as hashing, generalization, randomization, and masking to anonymize different types of data based on their sensitivity levels.

## Features
- **CSV Anonymization:** Anonymize sensitive data in CSV files based on column metadata specifying data types (date, number, string) and sensitivity types (identifier, insensitive, quasi-identifier, sensitive).
- **Text Anonymization:** Anonymize sensitive entities in text data using a transformer-based named entity recognition (NER) model. The server supports anonymizing various types of sensitive entities such as credit card numbers, email addresses, personal names, and more.

## Running the application
- Install the required dependencies: ```pip install -r requirements.txt```
- Start the Flask server: ```flask --app . run```
- The server will be running at http://localhost:5000.

## CSV Anonymization
To anonymize a CSV file, send a POST request to /api/anonymize/csv/ with the following payload:
- **file:** The CSV file to be anonymized.
- **column_metadata:** A JSON array containing column metadata objects with the following properties:
  - **name:** The name of the column.
  - **dataType:** The data type of the column (date, number, or string).
  - **sensitivityType:** The sensitivity type of the column (identifier, insensitive, quasi-identifier, or sensitive).
The server will return the anonymized CSV data as a JSON array of objects.

## Text Anonymization
To anonymize text data, send a POST request to /api/anonymize/text/ with the following payload:
- **text:(()) The text to be anonymized.
The server will return the anonymized text as a string.
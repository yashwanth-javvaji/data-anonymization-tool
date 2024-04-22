# Data Anonymization Tool
This project provides a comprehensive solution for anonymizing sensitive data in text and CSV files. It consists of a Flask backend server that handles the anonymization logic and a React frontend application that offers a user-friendly interface for interacting with the anonymization services.

## Features
- **Text Anonymization:** Anonymize sensitive entities in text data using a transformer-based named entity recognition (NER) model. The tool supports anonymizing various types of sensitive entities such as credit card numbers, email addresses, personal names, and more.
- **CSV Anonymization:** Anonymize sensitive data in CSV files based on column metadata specifying data types (date, number, string) and sensitivity types (identifier, insensitive, quasi-identifier, sensitive).

## Usage
- Choose the desired anonymization type (text or CSV) from the selector.
- For text anonymization, enter the text you want to anonymize and click the "Anonymize" button. The anonymized text will be displayed below.
- For CSV anonymization, upload the CSV file and specify the column metadata (name, data type, and sensitivity type). After providing the necessary information, click the "Anonymize" button. The anonymized data will be displayed in a grid view.
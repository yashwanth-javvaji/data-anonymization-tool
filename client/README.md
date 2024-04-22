# Data Anonymization Tool (UI)
This is a React-based frontend application for a data anonymization tool. It provides a user-friendly interface for anonymizing sensitive data in text or CSV files. The application communicates with a Flask backend server to perform the anonymization tasks.

## Features
- **Text Anonymization:** Anonymize sensitive entities in text data using a transformer-based named entity recognition (NER) model. The application supports anonymizing various types of sensitive entities such as credit card numbers, email addresses, personal names, and more.
- **CSV Anonymization:** Anonymize sensitive data in CSV files based on column metadata specifying data types (date, number, string) and sensitivity types (identifier, insensitive, quasi-identifier, sensitive).
- **Interactive UI:** The application provides an intuitive user interface with a selection option to choose between text or CSV anonymization. It also displays error messages and loading indicators for a better user experience.

## Running the application
- Install the dependencies: ```npm install```
- Start the development server: ```npm start```
- The application will be running at http://localhost:3000.

## Usage
- Choose the desired anonymization type (text or CSV) from the selector.
- For text anonymization, enter the text you want to anonymize and click the "Anonymize" button. The anonymized text will be displayed below.
- For CSV anonymization, upload the CSV file and specify the column metadata (name, data type, and sensitivity type). After providing the necessary information, click the "Anonymize" button. The anonymized data will be displayed in a grid view.
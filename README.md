# Data Anonymization Tool
The Data Anonymization Tool is a full-stack application built with Next.js and FastAPI that provides a user-friendly interface for anonymizing structured data (CSV files) and unstructured text data. The application allows users to upload CSV files, specify column metadata, and anonymize the data based on different sensitivity levels. It also supports anonymizing plain text data by detecting and masking sensitive information such as personal identifiers, credit card numbers, and more.

## Features
- **CSV Anonymization:** Upload CSV files and provide column metadata to anonymize structured data based on different data types (date, number, string) and sensitivity levels (identifier, insensitive, quasi-identifier, sensitive).
- **Text Anonymization:** Anonymize unstructured text data by detecting and masking sensitive information such as personal identifiers, credit card numbers, and other sensitive data types.
- **User-friendly Interface:** The Next.js frontend provides a clean and intuitive user interface for interacting with the anonymization features.
- **Serverless API:** The FastAPI backend serves as a serverless API for handling anonymization requests.

## Getting Started
Follow these steps to set up and run the Data Anonymization Tool on your local machine.

## Prerequisites
- Node.js (v20 or later)
- Python (v3.10 or later)
- npm (v10 or later)

## Installation
- Clone the repository: ```git clone https://github.com/yashwanth-javvaji/data-anonymization-tool```
- Navigate to the project directory: ```cd data-anonymization-tool```
- Install the required Python packages: ```pip3 install -r requirements.txt```
- Install the required Node.js packages: ```npm install```

## Running the Application
The Data Anonymization Tool consists of two components: the Next.js frontend and the FastAPI backend. You can run both components concurrently using the provided npm script: ```npm run dev```.
This command will start the Next.js development server and the FastAPI development server simultaneously. You can access the application at http://localhost:3000.

## API Endpoints
The FastAPI backend provides the following endpoints for anonymization:
- **POST /api/anonymize/csv:** Anonymize a CSV file based on provided column metadata.
- **POST /api/anonymize/text:** Anonymize plain text data by detecting and masking sensitive information.

## Configuration
The application uses environment variables for configuration. The following environment variables are available:
- **NEXT_PUBLIC_API_BASE_URL:** The base URL for the FastAPI backend. Defaults to http://localhost:8000/api.
You can set environment variables in the .env.local file in the project root directory.
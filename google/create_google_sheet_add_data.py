from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("google/.env")

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'google/fifth-bonbon-442814-r6-d9648c69b7f5.json'

# Define the necessary scopes for Google Sheets and Drive
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Authenticate using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialize Google Sheets and Drive API services
sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

def create_google_sheet_add_data(impression_counts):
    folder_id = os.getenv("GOOGLE_FOLDER_ID")

    # Log the impression_counts to see its structure
    print("[LOG] impression_counts:", impression_counts)

    # Create a new Google Sheet
    file_metadata = {
        'name': 'Patreon Impressions',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
    }

    # Get the current date and time
    now = datetime.now()
    formatted_time = now.strftime("%y%m%d_%H%M")

    # Update the file name with the current date and time
    file_metadata['name'] = f'Patreon Impressions_{formatted_time}'

    # If the folder ID is available, add it to the file's metadata
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Create the new Google Sheet file in Drive
    sheet = drive_service.files().create(body=file_metadata, fields='id').execute()
    sheet_id = sheet['id']
    print(f"Google Sheet created with ID: {sheet_id}")

    # Prepare the data for the sheet (post_id, impression_count, and post_url)
    try:
        values = [['Post ID', 'Impression Count', 'Post URL']]  # Header row
        values += [[item['post_id'], item['impression_count'], item['post_url']] for item in impression_counts]
    except KeyError as e:
        print(f"Error: Missing key {e} in impression_counts data.")
        return None

    # Write the data to the Google Sheet
    body = {
        'range': 'Sheet1!A1',
        'majorDimension': 'ROWS',
        'values': values,
    }

    try:
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        print("Data added to the Google Sheet.")
    except Exception as e:
        print(f"Error occurred while updating the Google Sheet: {e}")
        return None

    return sheet_id

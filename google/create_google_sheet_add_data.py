from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime

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

def create_google_sheet_add_data(impression_counts, folder_id=None):
    # Step 1: Create a new Google Sheet
    file_metadata = {
        'name': 'Patreon Impressions',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
    }
    # Get the current date and time
    now = datetime.now()
    formatted_time = now.strftime("%y%m%d_%H%M")

    # Update the file name with the current date and time
    file_metadata['name'] = f'Patreon Impressions_{formatted_time}'
    if folder_id:
        file_metadata['parents'] = [folder_id]

    sheet = drive_service.files().create(body=file_metadata, fields='id').execute()
    sheet_id = sheet['id']
    print(f"Google Sheet created with ID: {sheet_id}")

    # Step 2: Prepare data for the sheet
    values = [['Post Title', 'Impression Count']]  # Header row
    values += [[item['title'], item['impression_count']] for item in impression_counts]

    # Step 3: Write data to the sheet
    body = {
        'range': 'Sheet1!A1',
        'majorDimension': 'ROWS',
        'values': values,
    }
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    print("Data added to the Google Sheet.")

    return sheet_id

# Example usage
if __name__ == '__main__':
    # Mock impression data
    impression_counts = [
        {'title': 'Post 1', 'impression_count': 100},
        {'title': 'Post 2', 'impression_count': 250},
    ]

    # Replace with your target Google Drive folder ID
    folder_id = '1aVAXp4T89uh8yxTP4CGUPaSIwoweamRW'
    create_google_sheet_add_data(impression_counts, folder_id)

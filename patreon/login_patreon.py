import requests
import os
from dotenv import load_dotenv

def login_patreon():
    load_dotenv("patreon/.env")

    email = os.getenv("PATRON_EMAIL")
    password = os.getenv("PATRON_PASSWORD")

    base_url = 'https://www.patreon.com/api/auth'
    params = {
        'include': 'user.null',
        'fields[user]': '[]',
        'json-api-version': '1.0',
        'json-api-use-default-includes': 'false'
    }
    url = requests.Request('POST', base_url, params=params).prepare().url

    # Define the payload for the POST request
    payload = {
        'data': {
            'type': 'user',
            'attributes': {
                'email': {email},
                'password': {password}
            }
        }
    }

    # Define headers if needed
    headers = {
        'Content-Type': 'application/json',
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Fetch the session ID/cookie from the response
        session_id = response.cookies.get('session_id')
        print(f'Session ID: {session_id}')
    else:
        print(f'Failed to fetch session ID. Status code: {response.status_code}')
        print(f'Response: {response.text}')

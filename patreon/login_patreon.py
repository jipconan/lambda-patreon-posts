import requests
import os
from dotenv import load_dotenv

def login_patreon():
    load_dotenv("patreon/.env")

    email = os.getenv("PATRON_EMAIL")
    password = os.getenv("PATRON_PASSWORD")

    # Use a session to handle cookies
    session = requests.Session()

    base_url = 'https://www.patreon.com/api/auth'
    params = {
        'include': 'user.null',
        'fields[user]': '[]',
        'json-api-version': '1.0',
        'json-api-use-default-includes': 'false'
    }
    
    # Headers to simulate a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.patreon.com/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not:A-Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Step 1: Define the payload for the POST request (use your credentials)
    payload = {
        'data': {
            'type': 'genericPatreonApi',
            'attributes': {
                'patreon_auth': {
                    'email': email,
                    'password': password,
                    'allow_account_creation': False
                },
                'auth_context': 'auth'
            }
        }
    }
    
    # Step 2: Make the POST request to log in
    login_response = session.post(base_url, json=payload, headers=headers, params=params, allow_redirects=True)
    
    # Check if the login was successful
    if login_response.status_code == 200:
        print("[LOG] Successfully logged in to Patreon.")
        
        # Retrieve the session_id from the cookies
        session_id = session.cookies.get('session_id')
        
        if session_id:
            print(f"Retrieved Session ID: {session_id}")
        else:
            print("[ERROR] Session ID not found in cookies.")
        
        return session_id
    else:
        print(f"[ERROR] Failed to log in. Status code: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return None

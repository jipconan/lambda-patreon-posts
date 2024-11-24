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
        'User-Agent': 'PostmanRuntime/7.42.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.patreon.com/',
        'Origin': 'https://www.patreon.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'X-Requested-With': 'XMLHttpRequest', 
        'Cache-Control': 'max-age=0', 
    }
    
    # Step 1: Make an initial GET request to the login page to get cookies and potential CSRF token
    login_page = session.get('https://www.patreon.com/login', headers=headers, allow_redirects=True)
    
    if login_page.status_code != 200:
        print(f"Failed to load the login page. Status code: {login_page.status_code}")
        return None
    
    # Print cookies from the initial request for debugging
    print("[DEBUG] Cookies after GET request:", session.cookies.get_dict())

    # Step 2: Define the payload for the POST request (use your credentials)
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
    
    # Step 3: Make the POST request to log in, passing cookies from the login page
    login_response = session.post(base_url, json=payload, headers=headers, params=params, allow_redirects=True)
    
    # Print cookies after POST request for debugging
    print("[DEBUG] Cookies after POST request:", session.cookies.get_dict())
    
    # Check if the login was successful (Status 200 or your expected response code)
    if login_response.status_code == 200:
        print("[LOG] Successfully logged in to Patreon.")
        # Retrieve the CSRF token from the cookies
        csrf_token = session.cookies.get('csrf_token')  
        if csrf_token:
            print(f"Retrieved CSRF Token: {csrf_token}")
        else:
            print("CSRF token not found in cookies.")
        return csrf_token
    else:
        print(f"[ERROR] Failed to log in. Status code: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return None

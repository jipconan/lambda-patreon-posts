import cloudscraper
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("patreon/.env")

def fetch_session_id():
    email = os.getenv("PATRON_EMAIL")
    password = os.getenv("PATRON_PASSWORD")

    url = "https://www.patreon.com/api/auth?include=user.null&fields[user]=[]&json-api-version=1.0&json-api-use-default-includes=false"
    body = {
        "data": {
            "type": "genericPatreonApi",
            "attributes": {
                "patreon_auth": {
                    "email": email,
                    "password": password,
                    "allow_account_creation": False
                },
                "auth_context": "auth"
            },
            "relationships": {}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://www.patreon.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36",
    }

    # Create scraper
    scraper = cloudscraper.create_scraper()

    # Send POST request
    response = scraper.post(url, headers=headers, json=body)

    # Check response status
    if response.status_code == 200:
        # Extract session ID from cookies
        session_cookies = scraper.cookies
        session_id = session_cookies.get("session_id") 
        if session_id:
            return session_id  # Return the session ID for later use
        else:
            raise Exception("Session ID not found in cookies.")
    else:
        raise Exception(f"Failed to fetch session ID. HTTP Status Code: {response.status_code}, Response: {response.text}")

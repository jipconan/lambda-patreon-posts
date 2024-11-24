import requests

def fetch_impression():
    # base_url = f"https://www.patreon.com/api/posts/{post_id}"
    base_url = f"https://www.patreon.com/api/posts/116111967"
    params = {
        'fields[post]': 'impression_count'
    }
    headers = {
        # 'Cookie': f'csrf_token={csrf_token}',
        'Cookie': f'session_id=qIzqOoJoLfkPm4vXqKWhIWu7URPOafTCtEUpWUhgXr8;',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            impression_count = data.get('data', {}).get('attributes', {}).get('impression_count', None)
            
            # Log the impression count
            print(f"[LOG] Post ID: 116111967, Impressions: {impression_count}")
            return impression_count
        else:
            print(f"[ERROR] Failed to fetch impressions for Post ID: 116111967")
            print(f"[DEBUG] Status Code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] An error occurred: {str(e)}")
        return None

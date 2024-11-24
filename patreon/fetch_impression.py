import requests

def fetch_impression(post_id, session_id):
    base_url = "https://www.patreon.com/api/posts/"
    params = {
        'fields[post]': 'impression_count'
    }
    url = f"{base_url}{post_id}"
    headers = {
        'Cookie': f'session_id={session_id}'
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('attributes', {}).get('impression_count', None)
    else:
        response.raise_for_status()
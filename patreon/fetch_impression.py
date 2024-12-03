import requests

def fetch_impression(post_id, session_id):
    base_url = f"https://www.patreon.com/api/posts/{post_id}"
    params = {
        'fields[post]': 'impression_count,url'  # Fetch both impression count and url
    }
    headers = {
        'Cookie': f'session_id={session_id};',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            impression_count = data.get('data', {}).get('attributes', {}).get('impression_count', None)
            post_url = data.get('data', {}).get('attributes', {}).get('url', None)

            # Log the impression count and URL
            print(f"[LOG] Post ID: {post_id}, Impressions: {impression_count}, URL: {post_url}")

            # Return a dictionary with post_id, impression_count, and post_url
            return {
                "post_id": post_id,
                "impression_count": impression_count,
                "post_url": post_url
            }
        else:
            print(f"[ERROR] Failed to fetch impressions for Post ID: {post_id}")
            print(f"[DEBUG] Status Code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] An error occurred: {str(e)}")
        return None

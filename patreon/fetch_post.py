import requests
import os
from datetime import datetime

# Function to fetch today's posts from Patreon
def fetch_posts(period=datetime.now().date()):
    access_token = os.getenv("PATRON_API_KEY")
    campaign_id = os.getenv("PATRON_CAMPAIGN_ID")
    print("access_token:", access_token)

    # Make an API call to get today's posts
    response = requests.get(
        f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"fields[post]": "title,content,published_at,url"}
    )
    # print("Status Code:", response.status_code)
    # print("Response Headers:", response.headers)
    # print("Response Body:", response.text)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch posts: {response.content}")

    posts = response.json().get('data', [])

    # Filter posts published today and extract necessary fields
    today_posts = [
        {
            'title': post['attributes'].get('title'),
            'content': post['attributes'].get('content'),
            'url': post['attributes'].get('url')
        }
        for post in posts if post['attributes']['published_at'][:10] == str(period)
    ]
    
    return today_posts
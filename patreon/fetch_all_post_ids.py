import requests
import os
from dotenv import load_dotenv

load_dotenv("patreon/.env")

# Function to fetch all post IDs from Patreon
def fetch_all_post_ids():
    access_token = os.getenv("PATRON_API_KEY")
    campaign_id = os.getenv("PATRON_CAMPAIGN_ID")
    post_ids = []
    base_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    params = {
        "fields[post]": "url",  # Only fetch the 'url' field
        "page[count]": "10",    # Adjust for pagination size if needed
        "sort": "-published_at"
    }

    # Initial API call
    response = requests.get(base_url, headers={"Authorization": f"Bearer {access_token}"}, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch posts: {response.content}")

    # Process pages
    while response.status_code == 200:
        data = response.json()
        # Extract only the post ID from each URL
        post_ids.extend([
            post['attributes']['url'].split('/')[-1].split('-')[-1]  # Extract numeric ID after the last hyphen
            for post in data.get('data', [])
            if 'url' in post['attributes']
        ])
        
        next_page = data.get('links', {}).get('next')
        if not next_page:
            break  # No more pages, exit the loop

        # Fetch the next page
        response = requests.get(next_page, headers={"Authorization": f"Bearer {access_token}"})
    
    return post_ids  # Returning the array of post IDs

# Example usage
if __name__ == '__main__':
    post_ids = fetch_all_post_ids()
    print(f"Total number of post IDs fetched: {len(post_ids)}")
    print("Post IDs Array:")
    print(post_ids)  # This will output the array of post IDs

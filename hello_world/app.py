import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()  # Load environment variables

# Function to fetch today's posts from Patreon
def fetch_same_day_posts():
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
    today = datetime.now().date()

    # Filter posts published today and extract necessary fields
    today_posts = [
        {
            'title': post['attributes'].get('title'),
            'content': post['attributes'].get('content'),
            'url': post['attributes'].get('url')
        }
        for post in posts if post['attributes']['published_at'][:10] == str(today)
    ]
    
    return today_posts

# Function to post a message to Twitter with OAuth 1.0a
def post_to_twitter(message):
    twitter_api_url = "https://api.twitter.com/2/tweets"
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Initialize OAuth1 session
    twitter_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )
    
    # Create payload for the tweet
    payload = {"text": message}
    
    # Make the post request to Twitter API
    response = twitter_session.post(twitter_api_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to post to Twitter: {response.content}")

# Function to post a message to Discord
def post_to_discord(message, channel_id):
    discord_api_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    bot_token = os.getenv("DISCORD_BOT_TOKEN")

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    payload = {"content": message}

    response = requests.post(discord_api_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to post to Discord: {response.content}")

# Main lambda handler
def lambda_handler(event, context):
    try:
        channel_id = os.getenv("DISCORD_CHANNEL_ID")
        same_day_posts = fetch_same_day_posts()

        if same_day_posts:
            # Start the message with the header
            message = ("@everyone\n\n🚨 New Deck Profiles LIVE! 🚨\n\n"
                       "Our Advanced Deck Profiles are now available and ready for you to check out! 🎉\n\n")

            # Add formatted posts to the message
            for post in same_day_posts[:2]:  # Limit to two posts if required
                # Format each post with title and URL
                message += f"💙 {post['title']}:\n🔗 {post['url']}\n\n"
            
            # Finalize the message
            message += ("These guides are packed with advanced strategies to help you dominate the meta. "
                        "Go check them out now and level up your gameplay! 🔥")

            # Post the combined message to Twitter and Discord
            post_to_twitter(message)
            post_to_discord(message, channel_id)
            print(f"Posted to Twitter and Discord: {message}")
        else:
            print("No new posts today.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")



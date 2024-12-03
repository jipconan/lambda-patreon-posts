import json
from patreon.fetch_post import fetch_posts
from twitter.post_to_twitter import post_to_twitter
from discord.post_to_discord import post_to_discord
from src.create_message import create_message
from patreon.fetch_sessionid import fetch_session_id
from patreon.fetch_all_post_ids import fetch_all_post_ids
from patreon.fetch_impression import fetch_impression
from google.create_google_sheet_add_data import create_google_sheet_add_data

# Load the message template from the JSON file
def load_message_template():
    with open('src/message_template.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Main lambda handler
def lambda_handler(event, context):
    try:
        # Fetch posts for the current day
        same_day_posts = fetch_posts()

        if same_day_posts:
            # Load the message template
            json_template = load_message_template()

            # Generate the message for Twitter and Discord
            messageTwitter = create_message(json_template, same_day_posts, "twitter")
            messageDiscord = create_message(json_template, same_day_posts, "discord")
            
            # Post the combined message to Twitter and Discord
            post_to_twitter(messageTwitter)
            post_to_discord(messageDiscord)
            print(f"Posted to Twitter: {messageTwitter}")
            print(f"Posted to Discord: {messageDiscord}")
        else:
            print("No new posts today.")

        # Fetch all post IDs
        post_ids = fetch_all_post_ids()

        # Fetch session ID
        session_id = fetch_session_id()

        # List to store post IDs and impressions
        impression_data = []

        # Fetch impressions for each post and store the data
        for post_id in post_ids:
            impression = fetch_impression(post_id, session_id)
            if impression:
                impression_data.append(impression)

        # Add the data to Google Sheets
        if impression_data:
            sheet_id = create_google_sheet_add_data(impression_data)
            print(f"Data added to Google Sheet with ID: {sheet_id}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Test the lambda_handler function
lambda_handler("", "")

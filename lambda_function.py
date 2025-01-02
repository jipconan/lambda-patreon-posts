import json
from patreon.fetch_post import fetch_posts
from twitter.post_to_twitter import post_to_twitter
from discord.post_to_discord import post_to_discord
from src.create_message import create_message

# Load the message template from the JSON file
def load_message_template():
    with open('src/message_template.json', 'r', encoding='utf-8') as f: 
        return json.load(f)

# Main lambda handler
def lambda_handler(event, context):
    try:
        same_day_posts = fetch_posts()

        if same_day_posts:
            # Load the message template``
            json_template = load_message_template()

            # Generate the message using the template function
            messageTwitter = create_message(json_template, same_day_posts, "twitter")
            messageDiscord = create_message(json_template, same_day_posts, "discord")
            
            # Post the combined message to Twitter and Discord
            post_to_twitter(messageTwitter)
            post_to_discord(messageDiscord)
            print(f"Posted to Twitter: {messageTwitter}")
            print(f"Posted to Discord: {messageDiscord}")
        else:
            print("No new posts today.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# test locally
# lambda_handler("","")
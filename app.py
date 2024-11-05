from dotenv import load_dotenv
from patreon.fetch_post import fetch_posts
from twitter.post_to_twitter import post_to_twitter
from discord.post_to_discord import post_to_discord
from src.message_template import create_message 

load_dotenv()  # Load environment variables

# Main lambda handler
def lambda_handler(event, context):
    try:
        same_day_posts = fetch_posts()

        if same_day_posts:
            # Generate the message using the template function
            message = create_message(same_day_posts)
            
            # Post the combined message to Twitter and Discord
            post_to_twitter(message)
            post_to_discord(message)
            print(f"Posted to Twitter and Discord: {message}")
        else:
            print("No new posts today.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

lambda_handler("", "")

import json
from patreon.fetch_post import fetch_posts
from twitter.post_to_twitter import post_to_twitter
from discord.post_to_discord import post_to_discord
from src.create_message import create_message
from patreon.login_patreon import login_patreon
from patreon.fetch_impression import fetch_impression

# Load the message template from the JSON file
def load_message_template():
    with open('src/message_template.json', 'r', encoding='utf-8') as f: 
        return json.load(f)

# Main lambda handler
# def lambda_handler(event, context):
#     try:
#         same_day_posts = fetch_posts()

#         if same_day_posts:
#             # Load the message template``
#             json_template = load_message_template()

#             # Generate the message using the template function
#             messageTwitter = create_message(json_template, same_day_posts, "twitter")
#             messageDiscord = create_message(json_template, same_day_posts, "discord")
            
#             # Post the combined message to Twitter and Discord
#             post_to_twitter(messageTwitter)
#             post_to_discord(messageDiscord)
#             print(f"Posted to Twitter: {messageTwitter}")
#             print(f"Posted to Discord: {messageDiscord}")
#         else:
#             print("No new posts today.")
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# lambda_handler("","")

# def lambda_handler(event, context):
#     try:
#         # Log in to Patreon and fetch the CSRF token
#         print("[LOG] Logging in to Patreon...")
#         csrf_token = login_patreon()
        
#         if not csrf_token:
#             raise Exception("Failed to log in to Patreon. CSRF token not retrieved.")
        
#         print(f"[LOG] Retrieved CSRF Token: {csrf_token}")
        
#         # Prepare the response body as a string, using json.dumps() to serialize
#         response_body = {
#             "csrf_token": csrf_token
#         }

#         return {
#             "statusCode": 200,
#             "body": json.dumps(response_body)  # Serialize the dictionary to a JSON string
#         }
    
#     except Exception as e:
#         print(f"[EXCEPTION] Error occurred: {str(e)}")
#         return {
#             "statusCode": 500,
#             "body": json.dumps({"error": str(e)})  # Serialize error message to JSON string
#         }

def lambda_handler(event, context):
    try:
        # Fetch impressions directly using the hardcoded cookie
        print("[LOG] Fetching impressions...")
        impressions = fetch_impression()

        if not impressions:
            raise Exception("Failed to fetch impressions.")
        
        print(f"[LOG] Retrieved Impressions: {impressions}")
        
        # Prepare the response body as a string, using json.dumps() to serialize
        response_body = {
            "impressions": impressions
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body)  # Serialize the dictionary to a JSON string
        }
    
    except Exception as e:
        print(f"[EXCEPTION] Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})  # Serialize error message to JSON string
        }
    
lambda_handler("","")
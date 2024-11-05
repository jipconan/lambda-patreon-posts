# Function to create message from JSON template and fetched posts
def create_message(json_template, posts):
    # Patreon main URL
    base_url = "https://www.patreon.com"

    # Header
    message = json_template['header']
    
    # Append each post to the message
    for post in posts[:2]:  # Limit to two posts
        message += f"💙 {post['title']}:\n🔗 {base_url}{post['url']}\n\n"
    
    # Footer
    message += json_template['footer']
    return message

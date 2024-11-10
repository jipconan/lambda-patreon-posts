# Function to create message from JSON template and fetched posts
def create_message(json_template, posts, platform=""):
    # Patreon main URL
    base_url = "https://www.patreon.com"

    # Create empty message
    message = ""

    # Tag everyone only for Discord
    if platform == "discord":
        message += json_template['tagEveryone']

    # Header Start
    message += json_template['headerStart']

    # Add one or two titles in the header
    titles = ""
    if len(posts) > 1:
        titles = f"{posts[0]['title']} and {posts[1]['title']}"
    elif len(posts) == 1:
        titles = posts[0]['title']
    message += titles
    
    # Header End
    message += json_template['headerEnd']
    
    # Message, title: url
    for post in posts[:2]:  
        message += f"💙 {post['title']}:\n🔗 {base_url}{post['url']}\n\n"
    
    # Footer
    message += json_template['footer']

    # Add hashtags only if platform is Twitter
    if platform == "twitter":
        message += json_template['hashtags']

    return message

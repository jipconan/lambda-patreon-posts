def create_message(posts):
    # Patreon main url
    base_url = "https://www.patreon.com"

    # Start the message with the header
    message = ("@everyone\n\n🚨 New Deck Profiles LIVE! 🚨\n\n"
               "Our Advanced Deck Profiles are now available and ready for you to check out! 🎉\n\n")

    # Add formatted posts to the message
    for post in posts[:2]:  # Limit to two posts if required
        # Format each post with title and URL
        message += f"💙 {post['title']}:\n🔗 {base_url}{post['url']}\n\n"
    
    # Finalize the message
    message += ("These guides are packed with advanced strategies to help you dominate the meta. "
                "Go check them out now and level up your gameplay! 🔥")
    
    return message

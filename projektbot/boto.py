import urllib.request
import praw

reddit = praw.Reddit(
    client_id="SQH_PT8jleVf6tjGTHLOZg", #The client ID is the 14-character string listed just under “personal use script” for the desired developed application
    client_secret="3AAep9CO2KH7X6cRUaZH6RzUldtxQg", #The client secret is at least a 27-character string listed adjacent to secret for the application.
    user_agent="Test_BOT",
    username="Bot_741",
    password="Unob123456789",
)

subreddit = reddit.subreddit("aww")
count = 0

# Iterate through top submissions
for submission in subreddit.top(limit=None):

    # Get the link of the submission    url.endswith("jpg") or
    url = str(submission.url)

    # Check if the link is an image
    if url.endswith("jpeg") or url.endswith("png"):

        # Retrieve the image and save it in current folder
        urllib.request.urlretrieve(url, f"image{count}.jpg")
        count += 1

        # Stop once you have 10 images
        if count == 1:
            break

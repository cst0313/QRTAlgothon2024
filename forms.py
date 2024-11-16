import requests

# Step 1: Define the Google Form URL
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/viewform"  # Replace FORM_ID with the actual form ID

# Step 2: Define the form data
# Use the input field names (e.g., "entry.123456789") obtained from the form inspection
form_data = {
    "entry.123456789": "Henry Wu",    # Replace with the actual input name and value
    "entry.987654321": "henrywzh88@gmail.com",  # Example: Email field
    "entry.111213141": "Some Feedback"  # Example: Textarea field
}

# Step 3: Submit the form
response = requests.post(form_url, data=form_data)

# Step 4: Check the response
if response.status_code == 200:
    print("Form submitted successfully!")
else:
    print("Failed to submit the form. Status code:", response.status_code)

# Extract passcode
import logging
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = WebClient(token='xoxb-8020284472341-8025589293399-kNTNGNWRCBgD3GusUTPZDkKC')
# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = "C080P6M4DKL"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)

    conversation_history = result["messages"]

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))

# Regex pattern to extract file name and passcode
pattern = r"Data has just been released '([^']+)' the passcode is '([^']+)'.*"

# List to store results
results = []

# Iterate through messages
for message in conversation_history:
    if message['user'] == 'U080GCRATP1':
        match = re.search(pattern, message['text'])
        if match:
            file_name = match.group(1)
            passcode = match.group(2)
            results.append({'file_name': file_name, 'passcode': passcode})

# Print the results
for result in results:
    print(f"File Name: {result['file_name']}, Passcode: {result['passcode']}")
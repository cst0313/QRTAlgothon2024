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

# Get the latest result, if available
if results:
    latest_result = results[-1]  # Get the last entry
    f_file_name = latest_result['file_name']
    f_passcode = latest_result['passcode']
    
    print(f_file_name)
    print(f_passcode)
else:
    print("No results found.")
import json
from datetime import datetime, timezone

with open('example_conversation') as json_data:
  d = json.load(json_data)
  json_data.close()

  prev_timestamp = 0
  delay = 0

  for message in reversed(d['conversations'][0]['MessageList']):
    # Extract data from JSON
    author = message['from']
    timestamp = message['originalarrivaltime']
    content = message['content']

    # Parse delays and clean up message output
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    if prev_timestamp != 0:
      delay = (timestamp - prev_timestamp).total_seconds()
    prev_timestamp = timestamp
    content = content[3:-4]

    # Print to console for now
    # TODO: Output to file instead in object format
    print('Author:', author, 'Delay:', delay, 'Content:', content)

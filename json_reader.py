import json
from datetime import datetime, timezone

with open('example_conversation.json') as json_data:
    d = json.load(json_data)

prev_timestamp = None

with open("parsed_conversation.txt", 'w', encoding='utf-8') as output_file:
    for message in reversed(d['conversations'][0]['MessageList']):
        author = message['from']
        timestamp = message['originalarrivaltime']
        content = message['content']

        timestamp = datetime.strptime(
            timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)

        delay = 0
        if prev_timestamp is not None:
            delay = (timestamp - prev_timestamp).total_seconds()
        prev_timestamp = timestamp

        content = content[3:-4]

        record = {
            'Author': author,
            'Delay': delay,
            'Content': content
        }

        json.dump(record, output_file, ensure_ascii=False)
        output_file.write("\n")

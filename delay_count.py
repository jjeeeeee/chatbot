import json


def load_conversation(path):
  messages = []
  with open(path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
      messages.append(json.loads(line))
  return messages


if __name__ == "__main__":
  conv = load_conversation("parsed_conversation.txt")
  total_delay = 0
  for line in conv:
    total_delay += line['Delay']
  print(total_delay)

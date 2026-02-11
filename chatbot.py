import pyautogui
import pyperclip
import time
import ast

# ================= CONFIG =================

CONVERSATION_FILE = 'parsed_conversation.txt'
MY_AUTHOR = None   # CHANGE on the other device

COPY_X_RATIO = 898 / 2256
COPY_Y_RATIO = 1325 / 1504
WRITE_X_RATIO = 898 / 2256
WRITE_Y_RATIO = 1451 / 1504

POLL_INTERVAL = 1.0      # seconds between UI checks
MAX_WAIT_PER_MESSAGE = 300  # safety timeout

screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = True


# ================= HELPERS =================

def load_conversation(path):
    messages = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip():
                messages.append(ast.literal_eval(line))
    return messages


def read_latest_message():
    pyautogui.moveTo(screen_width * COPY_X_RATIO,
                     screen_height * COPY_Y_RATIO,
                     duration=0.2)
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    return pyperclip.paste().strip()


def send_message(message):
    pyautogui.moveTo(screen_width * WRITE_X_RATIO,
                     screen_height * WRITE_Y_RATIO,
                     duration=0.2)
    pyautogui.click()
    time.sleep(0.1)
    pyperclip.copy(message)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')


def wait_for_expected_message(expected_text):
  seen = read_latest_message()
  print(f"Expected: {expected_text}, Received: {seen}")
  if seen == expected_text:
    return True
  else:
    return False


def replay_conversation():
    conversation = load_conversation(CONVERSATION_FILE)

    i = 0
    while i < len(conversation):
        msg = conversation[i]
        author = msg['Author']
        delay = msg['Delay']
        content = msg['Content']

        if author == MY_AUTHOR:
            # SEND STATE
            print(f"[SEND] {content}")
            send_message(content)
            time.sleep(delay)
            i += 1

        else:
            # WAIT STATE
            msg_was_received = wait_for_expected_message(content)

            if msg_was_received:
                i += 1
            else:
                # Message hasn't been received yet, keep waiting
                print(f"[WAITING] Haven't received expected message yet. Expecting: {content}")
                time.sleep(5)


if __name__ == '__main__':
    replay_conversation()

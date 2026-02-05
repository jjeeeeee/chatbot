import pyautogui
import pyperclip
import time
import random
from google.genai import Client

# Parameters for running the script
CONVERSATION_DURATION = 60 * 60 * 4   # Currently 4 hours

# Relative positions (measured on my device)
COPY_X_RATIO = 798 / 2256
COPY_Y_RATIO = 1251 / 1504
WRITE_X_RATIO = 798 / 2256
WRITE_Y_RATIO = 1351 / 1504
# Device measurements
screen_width, screen_height = pyautogui.size()


# Create the client; GEMINI_API_KEY from environment
client = Client()


def determine_message(prompt):
  # Make a request to the API
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[{"text": prompt}]
  )
  return response.text


def get_response_delay():
    # Normal distribution with mean 5 seconds, std. dev 2 seconds
    delay = random.gauss(mu=5, sigma=2)
    return max(1, delay)  # Ensuring at least 1 second


def chatbot_loop():
  # Keeping track of last message seen and last message sent
  received_message_seen = ''
  message_sent = ''

  # Loop for specified amount of time
  # TODO: Change from True to CONVERSATION_DURATION time
  while True:
    # Safety: move mouse to top-left to abort
    pyautogui.FAILSAFE = True

    # Move mouse to message location and copy to clipboard
    pyautogui.PAUSE = 0.1
    pyautogui.moveTo(screen_width * COPY_X_RATIO, screen_height * COPY_Y_RATIO, duration=0.2)
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.1)

    # Read the message from the clipboard to the program
    text = pyperclip.paste()

    # Verifying that the copied message isn't the same one or one we sent
    if text != received_message_seen and text != message_sent:
      # Update received message
      received_message_seen = text

      # Clicking textbox in preparation to type a message
      pyautogui.PAUSE = 0.1
      pyautogui.moveTo(screen_width * WRITE_X_RATIO, screen_height * WRITE_Y_RATIO, duration=0.2)
      pyautogui.click(clicks=1, interval=0.1)
      time.sleep(0.1)

      # Determine how many messages to send in a single burst (between 1 and 5)
      burst_count = 1 #int(random.randint(1, 5))
      for _ in range(burst_count):
        # Determine the message to be sent
        message_sent = determine_message(text)

        # Write the message out and send it
        pyautogui.typewrite(message_sent)
        pyautogui.press('enter')

        # Wait a small amount of time between each burst message
        time.sleep(3)
      # Wait a random amount of time between each group of responses
      time.sleep(get_response_delay())
    else:
      # There have been no changes since you last sent a message, just wait
      time.sleep(5)


if __name__ == '__main__':
  chatbot_loop()
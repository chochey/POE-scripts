import pyautogui
import pygetwindow as gw
import time
import keyboard

# Name of the window to focus on, adjust if needed
window_name = "Path of Exile"

# Adjust the delay as needed
time_between_commands = 0.1  # seconds


def focus_on_window(window_name):
    try:
        # Find the window and bring it to the front
        window = gw.getWindowsWithTitle(window_name)[0]
        window.activate()
    except IndexError:
        print(f"No window with the title '{window_name}' found.")
        return False
    return True


# Function to exit the script
def exit_script():
    print("Exiting script.")
    exit(0)


# Set up the hotkey (Esc key) to exit the script
keyboard.add_hotkey("ctrl+shift+q", exit_script)

# Ensure the game window is in focus
if focus_on_window(window_name):
    for i in range(1, 900):
        # Simulate pressing 'Enter'
        pyautogui.press("enter")
        time.sleep(0.5)  # Short delay

        pyautogui.press("backspace")
        time.sleep(0.5)  # Short delay

        # Type '/trade' and the channel number
        pyautogui.typewrite(f"/trade {i}")
        time.sleep(0.5)  # Short delay

        # Simulate pressing 'Enter' to send the command
        pyautogui.press("enter")
        time.sleep(0.5)  # Short delay

        # Simulate pressing 'Enter' to send the command

        pyautogui.press("enter")
        time.sleep(0.5)  # Short delay

        # Your custom message
        custom_message = "$ T4 Asling 6 Div Portal Ready"

        # Type the custom message

        pyautogui.typewrite(custom_message)
        time.sleep(0.2)  # Short delay

        # Simulate pressing 'Enter' to send the message
        pyautogui.press("enter")

        # Wait before the next command
        time.sleep(time_between_commands)
else:
    print("Could not focus on the Path of Exile window.")

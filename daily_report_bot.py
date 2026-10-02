import pyautogui
import pyperclip
import time
import re
from datetime import datetime

pyautogui.PAUSE = 0.1

# ============================================================
# SETTINGS
# ============================================================

WEATHER_URL = (
    "https://www.accuweather.com/en/in/coimbatore/"
    "206673/current-weather/206673"
)

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1lojnblXmDWWglU4u6Q6-UbfsZ7XHnE1uwX_k8xa0eEU/"
    "edit?gid=0#gid=0"
)


# ============================================================
# STEP 1: OPEN GOOGLE CHROME USING SPOTLIGHT
# ============================================================

print("Opening Google Chrome...")

# Make sure modifier keys are released
pyautogui.keyUp("command")
pyautogui.keyUp("control")
pyautogui.keyUp("option")
pyautogui.keyUp("shift")

time.sleep(2)

# Open Spotlight
pyautogui.keyDown("command")
pyautogui.press("space")
pyautogui.keyUp("command")

# Give Spotlight plenty of time to appear
time.sleep(4)

# Type Chrome slowly
pyautogui.write(
    "Google Chrome",
    interval=0.3
)

time.sleep(2)

# Launch Chrome
pyautogui.press("enter")

# Wait for Chrome to fully open
time.sleep(8)

# ============================================================
# STEP 2: OPEN NEW TAB
# ============================================================

print("Opening new Chrome tab...")

pyautogui.hotkey("command", "t")

time.sleep(2)


# ============================================================
# STEP 3: OPEN ACCUWEATHER
# ============================================================

print("Opening AccuWeather...")

pyautogui.hotkey("command", "l")

time.sleep(2)

pyperclip.copy(WEATHER_URL)

pyautogui.hotkey("command", "v")

time.sleep(1)

pyautogui.press("enter")

# Wait for AccuWeather
time.sleep(8)


# ============================================================
# STEP 4: COPY WEBPAGE TEXT
# ============================================================

print("Reading weather information...")

pyautogui.hotkey("command", "a")

time.sleep(1)

pyautogui.hotkey("command", "c")

time.sleep(1)

page_text = pyperclip.paste()


# ============================================================
# STEP 5: EXTRACT TEMPERATURE
# ============================================================

match = re.search(r"\b(\d{1,2})°C\b", page_text)

if match:

    temperature = match.group(1) + "°C"

else:

    temperature = "Temperature not found"


print("Temperature:", temperature)


# ============================================================
# STEP 6: GET CURRENT DATE AND TIME
# ============================================================

current_datetime = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

today = datetime.now().strftime("%Y-%m-%d")

print("Date and Time:", current_datetime)


# ============================================================
# STEP 7: CREATE COMMENT
# ============================================================

if temperature != "Temperature not found":

    temp_value = int(
        re.search(r"\d+", temperature).group()
    )

    if temp_value >= 35:
        comment = "Very hot"

    elif temp_value >= 30:
        comment = "Warm"

    elif temp_value >= 25:
        comment = "Comfortable"

    else:
        comment = "Cool"

else:
    comment = "Unavailable"


# ============================================================
# STEP 8: OPEN GOOGLE SHEETS IN A NEW TAB
# ============================================================

print("Opening Google Sheets in a new tab...")

# Open a NEW Chrome tab
pyautogui.hotkey("command", "t")

time.sleep(3)

# Focus address bar
pyautogui.hotkey("command", "l")

time.sleep(2)

# Paste Google Sheets URL
pyperclip.copy(SHEET_URL)

pyautogui.hotkey("command", "v")

time.sleep(1)

pyautogui.press("enter")

# Wait for Google Sheets
time.sleep(8)


# ============================================================
# STEP 9: READ NEXT ROW
# ============================================================

try:

    with open("next_row.txt", "r") as file:
        next_row = int(file.read().strip())

except FileNotFoundError:

    next_row = 2

    with open("next_row.txt", "w") as file:
        file.write("2")


print("Entering data into row:", next_row)


# ============================================================
# STEP 10: SELECT THE CORRECT ROW
# ============================================================

# Google Sheets should open with A1 selected.
# Move down to the required row.

for _ in range(next_row - 1):

    pyautogui.press("down")

    time.sleep(0.2)

time.sleep(1)

# ============================================================
# STEP 11: ENTER DATA INTO CELLS
# ============================================================

print("Entering report data...")

# Make sure no modifier key is stuck
pyautogui.keyUp("command")
pyautogui.keyUp("control")
pyautogui.keyUp("option")
pyautogui.keyUp("shift")

time.sleep(1)

# -----------------------------
# A2 - Date & Time
# -----------------------------

pyautogui.write(
    current_datetime,
    interval=0.2
)

time.sleep(1)

# -----------------------------
# B2 - Temperature
# -----------------------------

pyautogui.press("tab")

time.sleep(1)

# Make absolutely sure Mac modifier keys are released
pyautogui.keyUp("command")
pyautogui.keyUp("control")
pyautogui.keyUp("option")
pyautogui.keyUp("shift")

time.sleep(1)

temperature_for_sheet = temperature.replace("°C", " C")

pyautogui.write(
    temperature_for_sheet,
    interval=0.4
)

time.sleep(1)



# -----------------------------
# C2 - Comment
# -----------------------------

pyautogui.press("tab")

time.sleep(1)

pyautogui.keyUp("command")
pyautogui.keyUp("control")
pyautogui.keyUp("option")
pyautogui.keyUp("shift")

time.sleep(1)

pyautogui.write(
    comment,
    interval=0.4
)

time.sleep(1)

## Finish the row
pyautogui.press("enter")

time.sleep(5)

print("Data entered successfully!")

# ============================================================
# STEP 13: UPDATE NEXT ROW
# ============================================================

next_row = next_row + 1

with open("next_row.txt", "w") as file:

    file.write(str(next_row))

print("Next row will be:", next_row)


# ============================================================
# STEP 14: SAVE SCREENSHOT
# ============================================================

print("Saving screenshot...")

# Close any open macOS menu before taking the screenshot
pyautogui.press("esc")

time.sleep(1)

screenshot_filename = f"daily_report_{today}.png"

pyautogui.screenshot().save(
    screenshot_filename
)

print("Screenshot saved:", screenshot_filename)

# ============================================================
# FINISHED
# ============================================================

print("--------------------------------")
print("DAILY REPORT BOT COMPLETED")
print("--------------------------------")
print("Date & Time :", current_datetime)
print("Temperature :", temperature)
print("Comment     :", comment)
print("Screenshot  :", screenshot_filename)
print("--------------------------------")
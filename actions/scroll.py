import pyautogui

pyautogui.FAILSAFE = True

def scroll_up(speed=3):
    pyautogui.scroll(speed)

def scroll_down(speed=3):
    pyautogui.scroll(-speed)

def click():
    pyautogui.click()

import pyautogui as auto
import keyboard
import time
cur = 328
key = keyboard
sentence = []
while True:
    key.wait("space") 
    while cur > 0:
        if key.is_pressed("2"):
            break
        res = cur-7
        sentence.extend([str(cur),"-","7","=",str(res) ])
        for i in sentence:
            for j in i:
                time.sleep(0.2)
                auto.press(j)
        auto.press("Enter")
        cur = cur - 7
        sentence.clear()
        time.sleep(1)

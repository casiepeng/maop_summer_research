import asyncio
import csv
import io
import json
from playwright.async_api import async_playwright
import app_search

#-----------------------------------------------------------------------------------
# Search through the links to see if they have: 
# 1. Eye tracking, put into the eye tracking app list AND sensors list
# (sensors are listed out, if there is none, the section doesn't exist!
# 2. If no eye tracking, check if have sensors. If so, put into sensors list
# 3. Paid versus Free as well!!! (4 json files????)
# 3. Else, ignore (continue)
# 
# Free examples: (get button instead of a button with $value)
# Amizon Prime Video example of one without sensors (would be ignored)
# https://www.meta.com/en-gb/experiences/amazon-prime-video/8379674632047815/
#
# Steam has eye tracking 
# https://www.meta.com/en-gb/experiences/steam-link/5841245619310585/ 
#
# Youtube has sensors but NO eye tracking
# https://www.meta.com/en-gb/experiences/youtube/2002317119880945/ 
# 
# Paid Example: 
# Virtual Desktop
# https://www.meta.com/en-gb/experiences/virtual-desktop/2017050365004772/ 
#-----------------------------------------------------------------------------------
async def search_links():
    # json files to add to
    # f_eye_tracking
    # p_eye_tracking
    # f_sensors
    # p_sensors

    json_files = {"f_eye_tracking.json", "p_eye_tracking.json", "f_sensors.json", "p_sensors.json"}
    #clear all json files
    for file in json_files:
        clear_json(file)

    #opens the links file to go through every app link
    with open('app_links.csv', 'r') as file: 
        csv_reader = csv.reader(file)
        i = 1
        for row in csv_reader:
            url = row[0].strip()
            if not url:
                continue
            print(f"line {i}")
            await app_search.scrape_app(url)  # just await the coroutine
            i = i + 1

def clear_json(filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)


asyncio.run(search_links())

        

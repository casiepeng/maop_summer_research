import asyncio
import json
import io
import csv
from playwright.async_api import async_playwright

#---------------------------------------------------------------------------
# goes into an individual app and figures out if it has eyetracking. 
# If it has eye tracking, it will then add it into the appropriate json file 
# Else, it will leave it. 
#---------------------------------------------------------------------------
# link = "https://www.meta.com/en-gb/experiences/steam-link/5841245619310585/"
async def scrape_app(url):
    # link = url
    app_data = []
    hasEyeTracking = False

    async with async_playwright() as p: 
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)

         # if confirmation button
        try:
            await page.get_by_role("button", name="Confirm").click(timeout=3000)
        except:
            pass  # ignore if button not present

        #searching for Eye tracking
        tracking = page.locator("text=Eye tracking").nth(0)
        eye_tracked = "No"
        title_clean = (await page.title()).strip()
        
        #checking to see if app is free or paid, takes from the html of the website
        free_button = page.locator("span.x1heor9g.x17gzxuv:has-text('Get')")
        free = "paid"
        if await free_button.count() >0 and await free_button.is_visible():
                free = "free"
        
        #check to see if app has sensors or not
        sensors = "No"
        sensor_exist = page.locator("div.x16g9bbj.xobpncf:has-text('Sensor & device data')")
        if await sensor_exist.is_visible():
             sensors = "Yes"


        if await tracking.is_visible():
            # print("found!")
            eye_tracked = "Yes"
            
            #code for putting into json file
        # else :
        #     print ("not found!")

        app_data.append({
                "title": title_clean,
                "url": url,
                "cost": free,
                "sensors": sensors,
                "eye tracking": eye_tracked
            })

            # 4 different json files to append app to:
            # f_eye_tracking
            # p_eye_tracking
            # f_sensors
            # p_sensors
            # (then we don't write into a file if doesn't meet criteria)

        if free == "free":
            if eye_tracked == "Yes": 
                write_json(app_data, "f_eye_tracking.json")
                write_json(app_data, "f_sensors.json")

            elif sensors == "Yes":
                write_json(app_data, "f_sensors.json")
        else:
            if eye_tracked == "Yes": 
                write_json(app_data, "p_eye_tracking.json")
                write_json(app_data, "p_sensors.json")

            elif sensors == "Yes":
                write_json(app_data, "p_sensors.json")            
        
        await browser.close()

def write_json(data, filename):
    try:
        # Try to load existing data
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/corrupt, start fresh
        existing_data = []

    # Append the new app data (single dictionary)
    existing_data.append(data)

    # Write the updated list back to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

# print(f"{link} link here")

# asyncio.run(scrape_app(link))
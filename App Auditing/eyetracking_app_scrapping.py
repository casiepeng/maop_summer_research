import asyncio
import json
import csv
from playwright.async_api import async_playwright

#------------------------------------------------------------------------------------------------------------
# playwrite is a web automation library allows for: 
# controling a browser, navigation of websites, click buttons, fill forms
# scrapping data as well
# Specifically imported the one with async capabilities. Don't need to start and stop!!!
# 
# asyncio helps with doing asynchronous programming. Rather than going the 
# linear path, it allows for efficiency by doing different tasks while
# "awaiting" other processes to not freeze the program. 
# NOT the same as multithreading!! (ex. a single barista that does other tasks 
# while waiting for things to finish) (multithreading would be multiple baristas
# doing their own individual tasks) 
#
# json objects (temporary) 
# used to store the data being scrapped. Key-value pairing structure.
# Ex. 
# {
#   "key": value,
#   "key2": value2    
# } 
# 
# idea: 
# scrape all apps from the meta app store (playwright) into a jason file (json) as json objects using the 
# asynchronous process (asyncio). 
# evemtually extract json objects to be read (use file reading capabilities)
# to write into an excel sheet. 
# want to be able to go into every app to find eye tracking eventually. (use other .py file!)
#------------------------------------------------------------------------------------------------------------

async def scrape_apps(url):
    app_data = []
    # url = "https://www.meta.com/en-gb/experiences/section/3878844519028756/" hard coding the url
    # https://www.meta.com/en-gb/experiences/section/3878844519028756/ "browse all" has more games
    # "https://www.meta.com/en-gb/experiences/section/3955297897903802/" # "browse all apps"
    try:
                # Try to load existing data
                    with open('apps.json', 'r', encoding='utf-8') as f:
                        app_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
                # If file doesn't exist or is empty/corrupt, start fresh
                    app_data = []

    async with async_playwright() as p:
        #launches a browser. this one is chrom
        #could have launched firefox with p.firefox or
        #safari with p.webkit
        #headless == True means it runs without showing a GUI window (makes this faster for automation)
        #if set to false, can see what is happening!!
        browser = await p.chromium.launch(headless=False)
        
        #opens a new tab/page in the browser where the navigation/scraping happens
        page = await browser.new_page()
        await page.goto(url) #goes to the URL... pretty self explanatory

        #try catch, tries to find the confirm button and clicks on it
        # try: 
        #     confirm_button = page.locator("text=Confirm")
        #     if await confirm_button.is_visible():
        #         await confirm_button.click()
        #         await page.wait_for_timeout(5000) 
        # except Exception as e: 
        #     print("No confirm button found:", e)

        # confirm the button
        await page.get_by_role("button", name="Confirm").click()

        # Scroll until all apps load and put into app_elements

        #target count is 993 apps plus offset
        target_count = 1004
        last_count = 0
        max_attempts = 10
        stagnant_attempts = 0

        while True:
            await page.mouse.wheel(0, 500)
            await page.wait_for_timeout(4000)

            #captures the links (apps) loaded after scrolling
            app_elements = await page.locator("a[href*='/experiences/']").all()
            current_count = len(app_elements)
            print(f"📦 Found {current_count} app elements...")

            #reaches the number of apps needed
            if current_count >= target_count:
                break

            #counter measure to not be in infinite loop
            if current_count == last_count:
                stagnant_attempts += 1
            else:
                stagnant_attempts = 0
                last_count = current_count

            if stagnant_attempts >= max_attempts:
                print("⚠️ No more new apps loaded after scrolling. Exiting.")
                break

        # Filter and extract app data
        #goes through the json objects (the apps)
        #seen ensures that no duplicate apps get saved! (set) and keeps track of urls
        seen = set()
        for app in app_elements:
            #gets the link from the html
            href = await app.get_attribute("href")
            #grabs the title of the link from the html 
            title = await app.inner_text()
            if not href or not title:
                continue

            #.strip() is a python method that gets rid of surrounding white space!
            title_clean = title.strip()
            
            skip_titles = {"Apps and games", "Home", "Games", "Apps", "Horizon+", "Wishlist",
                           "Worlds", "Sales"}
            
            if title_clean in skip_titles or len(title_clean) < 3:
                continue

            #ensures app is unique and adds
            if href not in seen:
                seen.add(href)
                # Append the new app data (single dictionary)
                app_data.append({
                    "title": title_clean,
                    "url": f"https://www.meta.com{href}"
                })
            
        #clean up
        await browser.close()
    return app_data

# Clear old output
with open("apps.json", "w", encoding="utf-8") as f:
    json.dump([], f, indent=2)

async def main():
    all_app_data = []
    seen_urls = set()
    urls = [
        "https://www.meta.com/en-gb/experiences/section/3878844519028756/",
        "https://www.meta.com/en-gb/experiences/section/3955297897903802/"
    ]

    #print(f"this is the app data so far: \n {all_app_data}")

    for url in urls:
        result = await scrape_apps(url)

        #print(f"after first scrape app data is: \n {result}")

        for app in result:
            if app['url'] not in seen_urls:
                seen_urls.add(app['url'])
                all_app_data.append(app)
    
    #print(f"second scraping app data: \n {all_app_data}")

    with open("apps.json", "w", encoding="utf-8") as f:
        json.dump(all_app_data, f, indent=2, ensure_ascii=False)

    with open("app_links.csv", "w", newline='') as f:
        writer = csv.writer(f)
        for app in all_app_data:
            writer.writerow([app['url']])

asyncio.run(main())



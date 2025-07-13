# imports
import asyncio
import io
import csv
from playwright.sync_api import sync_playwright

#-------------------------------------------------------------------------------
# Goes to the specific app link and finds the privacy policy
# Once it finds the privacy policy, it will get the privacy policy link
# That is all for this program. However, this will be tied with the other 
# Gen AI prompting scripts that will be written to prompt using this. 
#-------------------------------------------------------------------------------

def get_developer(url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)

        try:
            page.get_by_role("button", name="Confirm").click(timeout=5000)
        except:
            pass

        links = page.locator(".x16g9bbj.x17gzxuv.x3a6nna.xm5vtmc.x1t2x7uc.x1o1n6r0." +
                            "x1wsgf3v.x1c773n9.x1k03ns3.xpbi8i2.x9820fh.x1npfmwo." +
                            "xhj0du5.xrm2kyc.xjprkx4.xlu1awn.x12429cg.x6tc29j.xbq7h4v." +
                            "x6jdkww.xq9mrsl")
        count = links.count()
        index = 0
        for i in range(count):
            if links.nth(i).inner_text() == "Developer":
                index = i
                break
            

        #gets specifically the privacy policy

        search = page.locator(".x16g9bbj.x17gzxuv.x3a6nna.xm5vtmc.x1t2x7uc.x1o1n6r0." +
                            "x1wsgf3v.x1c773n9.x1k03ns3.xpbi8i2.x9820fh.x1npfmwo." +
                            "xhj0du5.xrm2kyc.xjprkx4.xlu1awn.x12429cg.x6tc29j.xbq7h4v." +
                            "x6jdkww.xq9mrsl").nth(index + 1)
        
        developer = search.inner_text()
        print(developer)
              
        browser.close()
        

        return developer
        # policy = page2.content()

        # with open("./privacy_policy.txt", "w", encoding="utf-8") as f: 
        #     f.write(policy)
        
        # browser.close()

#testing
#get_developer("https://www.meta.com/en-gb/experiences/immersed/2849273531812512/")

def non_meta_apps():
    #opens the links file to go through every app link
    meta_count = 0
    count = 0
    meta_apps = []
    with open('f_eye_tracking_links.csv', 'r') as file: 
            csv_reader = csv.reader(file)
            i = 1
            for row in csv_reader:
                url = row[0].strip()
                if not url:
                    continue
                print(f"line {i}")
                count = i
                if ("Facebook" in get_developer(url)) or ("Meta" in get_developer(url)) :
                    meta_count = meta_count + 1
                    meta_apps.append(url)
                i = i + 1    
    new_count = 0
    with open('p_eye_tracking_links.csv', 'r') as file: 
            csv_reader = csv.reader(file)
            i = 1
            for row in csv_reader:
                url = row[0].strip()
                if not url:
                    continue
                print(f"line {i}")
                new_count = i
                if ("Facebook" in get_developer(url)) or ("Meta" in get_developer(url)) :
                    meta_count = meta_count + 1
                    meta_apps.append(url)

                i = i + 1  

    print(f"There are {new_count + count} apps and there are {meta_count} meta apps")
    print(f"These are the apps without the meta apps: {new_count + count - meta_count}")
    print(meta_apps)
    return new_count + count - meta_count 

non_meta_apps()

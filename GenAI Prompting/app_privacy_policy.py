# imports
import asyncio
import io
from playwright.sync_api import sync_playwright

#-------------------------------------------------------------------------------
# Goes to the specific app link and finds the privacy policy
# Once it finds the privacy policy, it will get the privacy policy link
# That is all for this program. However, this will be tied with the other 
# Gen AI prompting scripts that will be written to prompt using this. 
#-------------------------------------------------------------------------------

def get_policy(url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)

        try:
            page.get_by_role("button", name="Confirm").click(timeout=5000)
        except:
            pass

        links = page.locator("a.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xdl72j9.xdt5ytf.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.xggy1nq.x1ja2u2z.x1t137rt.xt0psk2.x1bvjpef.xt0b8zv.xmy21w2.xj0a0fe")
        count = links.count()
        for i in range(count):
            print(links.nth(i).inner_text())

        #gets specifically the privacy policy

        link = page.locator("a.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xc5r6h4." + 
                            "xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5." +
                            "x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd." +
                            "x9f619.x1ypdohk.xdl72j9.xdt5ytf.x2lah0s.xe8uvvx." +
                            "xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli." +
                            "xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8." +
                            "xggy1nq.x1ja2u2z.x1t137rt.xt0psk2.x1bvjpef.xt0b8zv." +
                            "xmy21w2.xj0a0fe").nth(1)
        
        href = link.get_attribute("href")

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page2 = context.new_page()

        page2.goto(href)        
        browser.close()
        
        #print(href)

        return href
        # policy = page2.content()

        # with open("./privacy_policy.txt", "w", encoding="utf-8") as f: 
        #     f.write(policy)
        
        # browser.close()

#testing
get_policy("https://www.meta.com/en-gb/experiences/immersed/2849273531812512/")


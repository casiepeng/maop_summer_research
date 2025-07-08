# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
from google import genai

#-----------------------------------------------------------------------------------------------------------------
# Takes in a list of website links to different VR application privacy policies. The goal is to find the best 
# prompt to summarize details about sensors without adding any additional information ("Hallucinations") and 
# inaccurate information. 
#
# This algorithm then puts the responses in a txt file in the gemini policies folder (./gemini_policies_x) 
# the x signifies which prompt it took from (e.g. 1, 2, or 3) 
# 
# This model is specifically the Gemini 2.5 flash model most commonly used for Google Gemini. 
#-----------------------------------------------------------------------------------------------------------------

client = genai.Client()

links = {
    "https://appasset.xverse.cn/privacy/3dcinema/privacy_policy.pdf",
    "https://www.gorillatagvr.com/privacy-policy",
    "https://auravision.xyz/privacy-policy",
    "https://www.termsfeed.com/live/449e0122-ca8a-49b1-88dd-e4dc09a36838",
    "https://volucap.com/privacy-policy-voluverse/",
    "https://immerselearn.com/privacy-policy/",
    "https://www.rendever.com/alcove/privacy-policy",
    "https://policies.google.com/privacy",
    "https://hello.vrchat.com/privacy",
    "https://immersed.com/privacy"
}


def first_prompt():

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Go to the link provided below that contains a privacy policy." +
            " Summarize details regarding sensors in the privacy policy with visualizations and words to " +
            "make it understandable without getting rid of key information." +  
            "https://appasset.xverse.cn/privacy/3dcinema/privacy_policy.pdf"
    )
    # txt_file = 
    # with open(txt_file, ) 

    print(response.text)

def second_prompt():
    print("placeholder2")

def third_prompt():
    print("placeholder3")

first_prompt()
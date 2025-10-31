#imports
import google.generativeai as genai
from google import genai
import os

#-----------------------------------------------------------------------------------------------------------------
# Takes in a list of website links to different VR application privacy policies. The goal is to find the best 
# prompt to summarize details about sensors without adding any additional information ("Hallucinations") and 
# inaccurate information. 
#
# This algorithm then puts the responses in a txt file in the gemini policies folder (./gemini_policies_x) 
# the x signifies which prompt it took from (e.g. 1, 2, or 3) 
# 
# prompt 1 asks for text and visualizations summary without losing key information
# prompt 2 only asks for a summary (is a LLM so will purely be text) without losing key information
# prompt 3 asks the model to summarize (LLM so text) without losing key info AND without adding additional information (Hallucinations)
#
# PROMPT 4 IS THE ACTUAL POLICY!!! (in theory... hopefully gemini can get that done straightforward...)
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

prompts = [
    "Go to the link provided below that contains a privacy policy." +
    " Summarize details regarding sensors in the privacy policy with visualizations and words to " +
    "make it understandable without getting rid of key information.",
    "Go to the link provided below that contains a privacy policy." +
    " Summarize details regarding sensors in the privacy policy to make it understandable without " +
    "getting rid of key information.",
    "Go to the link provided below that contains a privacy policy." +
    " Summarize details regarding sensors in the privacy policy to make it understandable without " +
    "getting rid of key information and without adding additional information.",
    "Go to the link and extract the privacy policy without summarizing, without adding anything, and without " +
    " paraphrasing."
]


def prompt(prompt_index):
    for link in links:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents= prompts[prompt_index] + link
        )

        txt_file = "placeholder"

        if link.startswith("https://www."):
                    txt_file1 = link.removeprefix("https://www.")
                    txt_file = txt_file1[:txt_file1.find(".")] + ".txt"
        else:
                    txt_file1 = link.removeprefix("https://")
                    txt_file = txt_file1[:txt_file1.find(".")] + ".txt"
        
        with open(f'gemini_policies_{prompt_index + 1}/'+ txt_file, "w", encoding="utf-8") as f:
             print(txt_file)
             f.write(response.text)

        #print(response.text)

prompt_num = (int) (input("What prompt index (e.g. 0, 1, or 2) do you want to extract?\n " 
+ "(index 3 is no summarization and does policy extraction) : "))
prompt(prompt_num)
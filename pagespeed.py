import requests
import re
import pandas as pd
from ask_questions import answer_question
import numpy as np
import streamlit as st

df = pd.DataFrame()

def extract_url_from_string(string):
    return re.search("(?P<url>https?://[^\s]+)", string).group("url")

def process_data(data):
    audits = [data["lighthouseResult"]["audits"][i] for i in data["lighthouseResult"]["audits"]]
    audits_names = [i["title"] for i in audits]
    
    scoresdisplays = [data["lighthouseResult"]["audits"][i]["scoreDisplayMode"] for i in data["lighthouseResult"]["audits"]]

    df=pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    issues = []
    for i in audits:
        if i["scoreDisplayMode"] != "notApplicable" and (i["score"] != 1 and i["score"] != None) and "details" in i.keys() and i["scoreDisplayMode"] != "informative":
            title = i["title"]
            desc = i["description"]
            item = i["details"]["items"][0]
            typeOfIssue = i["details"]["type"]
            dicto = {"title": title, "description": desc, "item": item, "type": typeOfIssue}
            issues.append(dicto)
            print(title)
            print(i["details"]["type"])
            question = f"Title: {title}\nDescription: {desc}\nItem: {item}"
            #print(answer_question(df, question=question, debug=False))
            print("***********************************")
    return issues
            

def generate_response(website_url, url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed", api_key=st.secrets["page_speed_api_key"]):
    print("Website: " + website_url)
    print()
    name = website_url.split("//")[1].split(".")[1] # Get the name of the website

    params = {
        "url": website_url,
        "key": api_key,
        "category": ["performance", "accessibility", "best_practices", "seo"]
    }

    try:
        #output_file_path = f"Responses/{name}.json"
        if name not in st.session_state:
            st.session_state[name] = {}
        else:
            return st.session_state[name]
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for any request errors

        data = response.json()
        st.session_state[name] = data
        """
            with open(output_file_path, "w") as output_file:
                json.dump(data, output_file, indent=4)
        else:
            with open(output_file_path) as output_file:
                data = json.load(output_file)"""

        # Process the data as needed
        return data

    except requests.exceptions.RequestException as e:
        print("Error:", e)
#for i in list_of_urls:
#    data = generate_response(i)
#    process_data(data)
#https://chat.openai.com/share/71d7a128-b56d-4368-9eee-beda874e4200
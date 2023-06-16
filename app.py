import streamlit as st
from pagespeed import generate_response, process_data
from ask_questions import answer_question
import pandas as pd
import numpy as np

df = pd.DataFrame()
df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
# Set the title

if "button" not in st.session_state:
    st.session_state.button = False

st.title("PageSpeed Insights")

#start app
st.write("Enter a URL to get a PageSpeed Insights report")

# Get the URL from the user
url = st.text_input("URL", "https://www.google.com")

# If the user clicks the button

if st.button("Get Report") or st.session_state.button:
    with st.spinner(text="Collecting data..."):
        st.session_state.button = True
        # Get the response
        data = generate_response(url)
        # Process the data
        issues = process_data(data)
        # Show the data
        
        # for each issue in issues, make the title as an st.expander. When the expander is clicked, it shows its description and item. Also add a button in which the user can click to get the answer to the question.

    for index, issue in enumerate(issues):
        title = issue["title"]
        desc = issue["description"]
        item = issue["item"]
    
        with st.expander(title):
            st.write(desc)
            if st.button("Fix Issue", key=index):
                with st.spinner(text="Finding solution..."):
                    question = f"Title: {title}\nDescription: {desc}\nItem: {item}"
                    st.write(answer_question(df, question=issue["description"], debug=False))
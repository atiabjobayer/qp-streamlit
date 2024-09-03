import streamlit as st
import requests
import json

ACCESS_TOKEN = st.secrets["access_token"]
CLIENT_ID = st.secrets["client_id"]
API_ENDPOINT = "https://askrobot.azurewebsites.net"


def is_hebrew(char):
    return '\u0590' <= char <= '\u05FF'

def is_english(char):
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'

# Streamlit app
def main():
    st.title("Torah Search")
    st.markdown("""Demo of vector search within the Torah domain. The database currently includes the majority of the Rebbe's correspondence, in Hebrew and Yiddish.\\
    \\
    WhatsApp the bot at [+1 877 693-1021](https://wa.me/+18776931021)\\
    Contact the team at [info@trisso.com](mailto:info@trisso.com)\\
    [aitorah.org](https://aitorah.org/)""")
    # Text input for prompt
    prompt = st.text_input("Enter your prompt")

    # Dropdown for selection
    option = st.selectbox("Select an option", ["Answer", "Search"])

    # Button to submit
    if st.button("Submit"):
        if option == "Answer":
            # Call the Answer API
            response = call_answer_api(prompt)
            hebrew = is_hebrew(response[0])
            st.markdown(
                    f"<div style='text-align: {"right" if hebrew else "left"}; direction: {"rtl" if hebrew else "ltr"}'><h4>Answer</h4></div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                    f"<div style='text-align: {"right" if hebrew else "left"}; direction: {"rtl" if hebrew else "ltr"}'>{response}</h4></div>",
                    unsafe_allow_html=True,
                )
            st.divider()
            response = call_search_api(prompt)
            print(response)

            st.markdown(
                    f"<div style='text-align: right; direction: rtl;'><h4>Sources</h4></div>",
                    unsafe_allow_html=True,
                )
            
            index = 0

            for source in response:
                index = index + 1
                st.markdown(
                    f"<div style='text-align: right; direction: rtl;'><h4>{source['title']}</h4></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: right; direction: rtl;'>{source['text'].replace("\n", "<br>")}</h4></div>",
                    unsafe_allow_html=True,
                )

            

        elif option == "Search":
            # Call the Search API
            response = call_search_api(prompt)
            print(response)

            index = 0

            st.markdown(
                    f"<div style='text-align:right; direction:rtl'><h4>Search Result</h4></div>",
                    unsafe_allow_html=True,
                )
            for source in response:
                index = index + 1
                st.markdown(
                    f"<div style='text-align: right; direction: rtl;'><h4>{source['title']}</h4></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: right; direction: rtl;'>{source['text'].replace("\n", "<br>")}</h4></div>",
                    unsafe_allow_html=True,
                )
                # st.caption(source["text"])


# Function to call Answer API
def call_answer_api(prompt):
    # Replace with your actual API call
    response = requests.post(
        API_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        },
        json={
            "api": True,
            "engine": "answer",  # Use "answer" for RAG, "search" for searching
            "client": CLIENT_ID,
            "question": prompt,  # Your natural language query
        },
    )
    response_json = json.loads(response.text)
    print(response_json)
    return response_json["data"]["answer"]


# Function to call Search API
def call_search_api(prompt):
    # Replace with your actual API call
    response = requests.post(
        API_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        },
        json={
            "api": True,
            "engine": "search",  # Use "answer" for RAG, "search" for searching
            "client": CLIENT_ID,
            "question": prompt,  # Your natural language query
        },
    )
    response_json = json.loads(response.text)

    return response_json["data"]


if __name__ == "__main__":
    main()


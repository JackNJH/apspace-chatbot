import streamlit as st
import requests

# Define the URL of your Rasa server endpoint
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

# Function to send message to Rasa server and get response
def send_message_to_rasa(message):
    data = {"sender": "streamlit_user", "message": message}
    response = requests.post(RASA_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit UI components for chat interface
st.title("Demo Chatbot")

# Text input for user to type message
user_input = st.text_input("You:", "")

# Button to send message to Rasa
if st.button("Send"):
    if user_input:
        # Send user message to Rasa
        response = send_message_to_rasa(user_input)
        
        # Display Rasa bot responses
        if response:
            for r in response:
                st.text("Bot: {}".format(r['text']))
        else:
            st.error("Error communicating with Rasa server")

import streamlit as st
from emojify import emojify_text

# Set title for the web app
st.title("Emojify Me 2.0 - Context-Aware Emoji Bot")
st.sidebar.header("Settings")

# Mood selection
mood = st.sidebar.selectbox("Select Mood:", ["default", "funny", "sarcastic", "motivational", "cute", "excited"])

# User input options
option = st.sidebar.radio("Select Option", ["Text Input", "File Upload"])

if option == "Text Input":
    # User types a sentence
    input_text = st.text_area("Enter your text", "Type something here...")

    if st.button("Emojify"):
        emojified_text = emojify_text(input_text, mood=mood)
        st.write("Emojified Text:")
        st.write(emojified_text)

elif option == "File Upload":
    # File upload
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        if st.button("Emojify File"):
            emojified_text = emojify_text(text, mood=mood)
            st.write("Emojified Text:")
            st.write(emojified_text)

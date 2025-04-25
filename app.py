import streamlit as st
from emojify import emojify_text

# Set page config for better appearance
st.set_page_config(page_title="Emojify Me 2.0", page_icon="😊", layout="wide")

# Set title and header
st.title("Emojify Me 2.0 - Context-Aware Emoji Bot")
st.markdown("Transform your text with mood-based emojis! 🎉")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    mood = st.selectbox("Select Mood:", ["default", "funny", "sarcastic", "motivational", "cute", "excited"])
    option = st.radio("Select Input Method", ["Text Input", "File Upload"])

# Main content
if option == "Text Input":
    input_text = st.text_area("Enter your text", placeholder="Type your text here...", height=200)
    
    if st.button("Emojify", key="text_emojify"):
        if input_text.strip():
            try:
                emojified_text = emojify_text(input_text, mood=mood)
                st.subheader("Emojified Result:")
                st.markdown(emojified_text)
            except Exception as e:
                st.error(f"Error processing text: {str(e)}")
        else:
            st.warning("Please enter some text to emojify!")

elif option == "File Upload":
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            text = uploaded_file.read().decode("utf-8")
            if st.button("Emojify File", key="file_emojify"):
                if text.strip():
                    emojified_text = emojify_text(text, mood=mood)
                    st.subheader("Emojified Result:")
                    st.markdown(emojified_text)
                else:
                    st.warning("The uploaded file is empty!")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
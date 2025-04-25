import streamlit as st
from emojify import emojify_text
import re

# Set page config
st.set_page_config(page_title="Emojify Me 2.0", page_icon="😊", layout="wide")

# Initialize session state for input history
if "input_history" not in st.session_state:
    st.session_state.input_history = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Set title and header
st.title("Emojify Me 2.0 - Context-Aware Emoji Bot")
st.markdown("Transform your text with mood-based emojis! 🎉")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    mood = st.selectbox("Select Mood:", ["default", "funny", "sarcastic", "motivational", "cute", "excited"])
    emoji_intensity = st.slider("Emoji Intensity", 1, 3, 2, help="1: Low, 2: Medium, 3: High")
    output_format = st.selectbox("Output Format:", ["Paragraph", "Bulleted List", "Highlighted Emojis"])
    use_sentiment_emoji = st.checkbox("Add Sentiment Emojis", value=True)

# Main content
if st.session_state.current_input:
    st.text_area("Current Input", value=st.session_state.current_input, key="current_input_display", disabled=True)

option = st.radio("Select Input Method", ["Text Input", "File Upload"], horizontal=True)

if option == "Text Input":
    input_text = st.text_area("Enter your text", placeholder="Type your text here...", height=200, key="text_input")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Emojify", key="text_emojify"):
            if input_text.strip():
                try:
                    st.session_state.input_history.append(input_text)
                    st.session_state.current_input = input_text
                    emojified_text = emojify_text(input_text, mood=mood, intensity=emoji_intensity, use_sentiment=use_sentiment_emoji)
                    st.session_state.emojified_result = emojified_text
                    st.session_state.output_format = output_format
                except Exception as e:
                    st.error(f"Error processing text: {str(e)}")
            else:
                st.warning("Please enter some text to emojify!")
    with col2:
        if st.button("Undo", key="undo"):
            if st.session_state.input_history:
                st.session_state.input_history.pop()
                st.session_state.current_input = st.session_state.input_history[-1] if st.session_state.input_history else ""
                st.session_state.emojified_result = None
    with col3:
        if st.button("Reset", key="reset"):
            st.session_state.input_history = []
            st.session_state.current_input = ""
            st.session_state.emojified_result = None

elif option == "File Upload":
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            text = uploaded_file.read().decode("utf-8")
            st.session_state.current_input = text
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Emojify File", key="file_emojify"):
                    if text.strip():
                        st.session_state.input_history.append(text)
                        emojified_text = emojify_text(text, mood=mood, intensity=emoji_intensity, use_sentiment=use_sentiment_emoji)
                        st.session_state.emojified_result = emojified_text
                        st.session_state.output_format = output_format
                    else:
                        st.warning("The uploaded file is empty!")
            with col2:
                if st.button("Undo", key="file_undo"):
                    if st.session_state.input_history:
                        st.session_state.input_history.pop()
                        st.session_state.current_input = st.session_state.input_history[-1] if st.session_state.input_history else ""
                        st.session_state.emojified_result = None
            with col3:
                if st.button("Reset", key="file_reset"):
                    st.session_state.input_history = []
                    st.session_state.current_input = ""
                    st.session_state.emojified_result = None
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Display emojified result
if "emojified_result" in st.session_state and st.session_state.emojified_result:
    st.subheader("Emojified Result:")
    if st.session_state.output_format == "Bulleted List":
        for sentence in st.session_state.emojified_result.split('\n\n'):
            st.markdown(f"- {sentence}")
    elif st.session_state.output_format == "Highlighted Emojis":
        highlighted_text = re.sub(r'([😀-🙏🌀-🦓]+)', r'**_\1_**', st.session_state.emojified_result)
        st.markdown(highlighted_text)
    else:
        st.markdown(st.session_state.emojified_result)
    
    # Download button for result
    st.download_button(
        label="Download Result",
        data=st.session_state.emojified_result,
        file_name="emojified_text.txt",
        mime="text/plain"
    )
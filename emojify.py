import nltk
from textblob import TextBlob
import streamlit as st

# Ensure necessary NLTK data is downloaded
nltk.download("punkt")

# Enhanced Emoji Dictionary with More Keywords and Moods
emoji_dict = {
    "happy": {"default": "😊", "funny": "😂", "sarcastic": "🙄", "motivational": "💪", "cute": "🥰", "excited": "😆"},
    "sad": {"default": "😢", "funny": "😭", "sarcastic": "😑", "motivational": "😔", "cute": "😞", "angry": "😠"},
    "love": {"default": "❤️", "funny": "💔", "sarcastic": "💘", "motivational": "💖", "cute": "😍", "affection": "😘"},
    "angry": {"default": "😠", "funny": "🤬", "sarcastic": "😤", "motivational": "🔥", "cute": "😡", "frustrated": "😡"},
    "excited": {"default": "😆", "funny": "😜", "sarcastic": "😏", "motivational": "🙌", "cute": "🤩", "super": "🥳"},
    "tired": {"default": "😩", "funny": "😴", "sarcastic": "😑", "motivational": "😓", "cute": "🥱", "exhausted": "🛌"},
    "study": {"default": "📚", "funny": "👨‍💻", "sarcastic": "📝", "motivational": "📖", "cute": "📚", "focused": "💡"},
    "exam": {"default": "📝", "funny": "🤯", "sarcastic": "😴", "motivational": "🔪", "cute": "📅", "stress": "😰"},
    "free": {"default": "🎉", "funny": "🕺", "sarcastic": "😌", "motivational": "💃", "cute": "🎊", "relaxed": "🌞"},
    "confused": {"default": "😕", "funny": "😵", "sarcastic": "🤷‍♂️", "motivational": "🤔", "cute": "🙄", "baffled": "🌀"},
    "sleep": {"default": "😴", "funny": "💀", "sarcastic": "🛌", "motivational": "💭", "cute": "😪", "dreaming": "🌙"},
    "bored": {"default": "🥱", "funny": "😑", "sarcastic": "🙃", "motivational": "🕰️", "cute": "🌀", "restless": "🛋️"},
    "coffee": {"default": "☕", "funny": "🍵", "sarcastic": "🥤", "motivational": "🔥", "cute": "☕️", "energized": "💪"},
    "food": {"default": "🍲", "funny": "🍕", "sarcastic": "🍔", "motivational": "🥗", "cute": "🍩", "hungry": "🍔"},
    "music": {"default": "🎶", "funny": "🎧", "sarcastic": "🎼", "motivational": "🎸", "cute": "🎤", "relaxing": "🎶"},
    "dance": {"default": "💃", "funny": "🕺", "sarcastic": "💁‍♀️", "motivational": "💪", "cute": "🕺", "party": "💃"},
    "assignment": {"default": "📄", "funny": "📝", "sarcastic": "🧾", "motivational": "🏆", "cute": "📚", "study": "📚"},
    "deadline": {"default": "⏰", "funny": "⌛", "sarcastic": "⏳", "motivational": "⏱️", "cute": "⏰", "pressure": "⚡"},
    "friends": {"default": "👯", "funny": "👯‍♂️", "sarcastic": "🤔", "motivational": "👫", "cute": "👬", "bestie": "👭"},
    "success": {"default": "🏆", "funny": "🎉", "sarcastic": "🥳", "motivational": "💯", "cute": "💎", "achieved": "🥇"},
    "thankful": {"default": "🙏", "funny": "💁‍♀️", "sarcastic": "🙄", "motivational": "👏", "cute": "❤️", "grateful": "🦋"},
    "party": {"default": "🎉", "funny": "🎈", "sarcastic": "🎉", "motivational": "💥", "cute": "🎊", "celebrate": "🍾"},
    "grateful": {"default": "🙏", "funny": "🙇‍♂️", "sarcastic": "😏", "motivational": "🤝", "cute": "🦋", "appreciate": "🌻"},
    "adventure": {"default": "🌍", "funny": "🚶‍♂️", "sarcastic": "🏞️", "motivational": "🗺️", "cute": "🎒", "exploring": "🌄"},
    "travel": {"default": "✈️", "funny": "🚂", "sarcastic": "🛳️", "motivational": "🚗", "cute": "🏖️", "vacation": "🗺️"},
    "nature": {"default": "🌿", "funny": "🍃", "sarcastic": "🌳", "motivational": "🌸", "cute": "🌺", "serene": "🌻"}
}

# Function to clean text (remove punctuation, lowercase it)
def clean_text(text):
    text = text.lower()
    return ''.join([char for char in text if char.isalnum() or char.isspace()])

# Function to emojify text
def emojify_text(text, mood="default"):
    text = clean_text(text)
    blob = TextBlob(text)
    tokens = nltk.word_tokenize(text)
    result = []

    for word in tokens:
        clean = word.lower()
        if clean in emoji_dict:
            result.append(word + " " + emoji_dict[clean].get(mood, emoji_dict[clean]["default"]))
        else:
            result.append(word)

    # Check sentiment and append emoji based on mood
    sentiment = blob.sentiment.polarity
    if sentiment > 0.3:
        result.append(emoji_dict["happy"].get(mood, emoji_dict["happy"]["default"]))
    elif sentiment < -0.3:
        result.append(emoji_dict["sad"].get(mood, emoji_dict["sad"]["default"]))

    return ' '.join(result)

# Streamlit UI
st.title("Emojify Me 2.0 - The Emoji Generator App")
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

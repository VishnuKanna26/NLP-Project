import nltk
from textblob import TextBlob
import re

# Download required NLTK data
try:
    nltk.download("punkt", quiet=True)
except Exception as e:
    print(f"Error downloading NLTK data: {str(e)}")

# Enhanced Emoji Dictionary
emoji_dict = {
    "happy": {"default": "😊", "funny": "😂", "sarcastic": "🙄", "motivational": "💪", "cute": "🥰", "excited": "😆"},
    "sad": {"default": "😢", "funny": "😭", "sarcastic": "😑", "motivational": "😔", "cute": "😞", "excited": "😩"},
    "love": {"default": "❤️", "funny": "💖", "sarcastic": "💘", "motivational": "💞", "cute": "😍", "excited": "😘"},
    "angry": {"default": "😣", "funny": "🤬", "sarcastic": "😤", "motivational": "🔥", "cute": "😣", "excited": "😤"},
    "excited": {"default": "😆", "funny": "😜", "sarcastic": "😏", "motivational": "🙌", "cute": "🤩", "excited": "🥳"},
    "tired": {"default": "😩", "funny": "😴", "sarcastic": "😑", "motivational": "😓", "cute": "🥱", "excited": "🛌"},
    "study": {"default": "📚", "funny": "👨‍💻", "sarcastic": "📝", "motivational": "📖", "cute": "📚", "excited": "💡"},
    "exam": {"default": "📝", "funny": "🤯", "sarcastic": "😴", "motivational": "🎯", "cute": "📅", "excited": "😰"},
    "free": {"default": "🎉", "funny": "🕺", "sarcastic": "😌", "motivational": "💃", "cute": "🎊", "excited": "🌞"},
    "confused": {"default": "😕", "funny": "😵", "sarcastic": "🤷", "motivational": "🤔", "cute": "🙄", "excited": "🌀"},
    "sleep": {"default": "😴", "funny": "💤", "sarcastic": "🛌", "motivational": "💭", "cute": "😪", "excited": "🌙"},
    "bored": {"default": "🥱", "funny": "😑", "sarcastic": "🙃", "motivational": "🕰️", "cute": "🌀", "excited": "🛋️"},
    "coffee": {"default": "☕", "funny": "🍵", "sarcastic": "🥤", "motivational": "🔥", "cute": "☕", "excited": "⚡"},
    "food": {"default": "🍽️", "funny": "🍕", "sarcastic": "🍔", "motivational": "🥗", "cute": "🍰", "excited": "🍽️"},
    "music": {"default": "🎶", "funny": "🎧", "sarcastic": "🎼", "motivational": "🎸", "cute": "🎤", "excited": "🔊"},
    "dance": {"default": "💃", "funny": "🕺", "sarcastic": "🙆", "motivational": "🩰", "cute": "🕺", "excited": "💃"},
    "assignment": {"default": "📄", "funny": "📝", "sarcastic": "🧾", "motivational": "🏆", "cute": "📚", "excited": "📚"},
    "deadline": {"default": "⏰", "funny": "⌛", "sarcastic": "⏳", "motivational": "⏱️", "cute": "⏰", "excited": "⚡"},
    "friends": {"default": "👯", "funny": "👯‍♂️", "sarcastic": "🤝", "motivational": "👬", "cute": "👭", "excited": "👯"},
    "success": {"default": "🏆", "funny": "🎉", "sarcastic": "🥳", "motivational": "💯", "cute": "💎", "excited": "🥇"},
    "thankful": {"default": "🙏", "funny": "🙌", "sarcastic": "😏", "motivational": "👏", "cute": "❤️", "excited": "🙏"},
    "party": {"default": "🎉", "funny": "🎈", "sarcastic": "🥂", "motivational": "💥", "cute": "🎊", "excited": "🍾"},
    "grateful": {"default": "🙏", "funny": "🙇", "sarcastic": "😉", "motivational": "🤝", "cute": "🦋", "excited": "🌟"},
    "adventure": {"default": "🌍", "funny": "🚶", "sarcastic": "🏞️", "motivational": "🗺️", "cute": "🎒", "excited": "🌄"},
    "travel": {"default": "✈️", "funny": "🚂", "sarcastic": "🛳️", "motivational": "🚗", "cute": "🏖️", "excited": "🗺️"},
    "nature": {"default": "🌿", "funny": "🌴", "sarcastic": "🌳", "motivational": "🌸", "cute": "🌺", "excited": "🌻"}
}

def emojify_text(text, mood="default"):
    if not text or not isinstance(text, str):
        return "No valid text provided"
    
    # Split text into sentences while preserving punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    result_sentences = []

    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Tokenize while preserving punctuation
        tokens = nltk.word_tokenize(sentence)
        result_tokens = []
        blob = TextBlob(sentence)
        
        for token in tokens:
            # Check if token is a word (not punctuation)
            if re.match(r'\w+', token.lower()):
                clean = token.lower()
                if clean in emoji_dict:
                    emoji = emoji_dict[clean].get(mood, emoji_dict[clean]["default"])
                    result_tokens.append(f"{token}{emoji}")
                else:
                    result_tokens.append(token)
            else:
                # Preserve punctuation
                result_tokens.append(token)
        
        # Join tokens back into sentence
        emojified_sentence = ' '.join(result_tokens)
        
        # Add sentiment-based emoji at sentence end
        sentiment = blob.sentiment.polarity
        if sentiment > 0.3:
            emojified_sentence += f" {emoji_dict['happy'].get(mood, emoji_dict['happy']['default'])}"
        elif sentiment < -0.3:
            emojified_sentence += f" {emoji_dict['sad'].get(mood, emoji_dict['sad']['default'])}"
            
        result_sentences.append(emojified_sentence)
    
    # Join sentences with proper spacing
    return '\n\n'.join(result_sentences)
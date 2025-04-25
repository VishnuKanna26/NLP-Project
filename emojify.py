import nltk
from textblob import TextBlob
import re

# Download required NLTK data
try:
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)
except Exception as e:
    print(f"Error downloading NLTK data: {str(e)}")

# Enhanced Emoji Dictionary with Synonyms
emoji_dict = {
    "happy": {"default": " 😊", "funny": " 😂", "sarcastic": " 🙄", "motivational": " 💪", "cute": " 🥰", "excited": " 😆", "synonyms": ["joyful", "cheerful", "glad"]},
    "sad": {"default": " 😢", "funny": " 😭", "sarcastic": " 😑", "motivational": " 😔", "cute": " 😞", "excited": " 😩", "synonyms": ["unhappy", "sorrowful", "down"]},
    "love": {"default": " ❤️", "funny": " 💖", "sarcastic": " 💘", "motivational": " 💞", "cute": " 😍", "excited": " 😘", "synonyms": ["adore", "cherish", "affection"]},
    "angry": {"default": " 😣", "funny": " 🤬", "sarcastic": " 😤", "motivational": " 🔥", "cute": " 😣", "excited": " 😤", "synonyms": ["mad", "furious", "irritated"]},
    "excited": {"default": " 😆", "funny": " 😜", "sarcastic": " 😏", "motivational": " 🙌", "cute": " 🤩", "excited": " 🥳", "synonyms": ["thrilled", "eager", "enthusiastic"]},
    "tired": {"default": " 😩", "funny": " 😴", "sarcastic": " 😑", "motivational": " 😓", "cute": " 🥱", "excited": " 🛌", "synonyms": ["exhausted", "fatigued", "weary"]},
    "study": {"default": " 📚", "funny": " 👨‍💻", "sarcastic": " 📝", "motivational": " 📖", "cute": " 📚", "excited": " 💡", "synonyms": ["learn", "research", "read"]},
    "exam": {"default": " 📝", "funny": " 🤯", "sarcastic": " 😴", "motivational": " 🎯", "cute": " 📅", "excited": " 😰", "synonyms": ["test", "quiz", "assessment"]},
    "free": {"default": " 🎉", "funny": " 🕺", "sarcastic": " 😌", "motivational": " 💃", "cute": " 🎊", "excited": " 🌞", "synonyms": ["liberated", "available", "unrestrained"]},
    "confused": {"default": " 😕", "funny": " 😵", "sarcastic": " 🤷", "motivational": " 🤔", "cute": " 🙄", "excited": " 🌀", "synonyms": ["puzzled", "bewildered", "perplexed"]},
    "sleep": {"default": " 😴", "funny": " 💤", "sarcastic": " 🛌", "motivational": " 💭", "cute": " 😪", "excited": " 🌙", "synonyms": ["rest", "nap", "slumber"]},
    "bored": {"default": " 🥱", "funny": " 😑", "sarcastic": " 🙃", "motivational": " 🕰️", "cute": " 🌀", "excited": " 🛋️", "synonyms": ["uninterested", "tedious", "dull"]},
    "coffee": {"default": " ☕", "funny": " 🍵", "sarcastic": " 🥤", "motivational": " 🔥", "cute": " ☕", "excited": " ⚡", "synonyms": ["tea", "espresso", "latte"]},
    "food": {"default": " 🍽️", "funny": " 🍕", "sarcastic": " 🍔", "motivational": " 🥗", "cute": " 🍰", "excited": " 🍽️", "synonyms": ["meal", "dish", "cuisine"]},
    "music": {"default": " 🎶", "funny": " 🎧", "sarcastic": " 🎼", "motivational": " 🎸", "cute": " 🎤", "excited": " 🔊", "synonyms": ["song", "tune", "melody"]},
    "dance": {"default": " 💃", "funny": " 🕺", "sarcastic": " 🙆", "motivational": " 🩰", "cute": " 🕺", "excited": " 💃", "synonyms": ["boogie", "groove", "sway"]},
    "assignment": {"default": " 📄", "funny": " 📝", "sarcastic": " 🧾", "motivational": " 🏆", "cute": " 📚", "excited": " 📚", "synonyms": ["task", "homework", "project"]},
    "deadline": {"default": " ⏰", "funny": " ⌛", "sarcastic": " ⏳", "motivational": " ⏱️", "cute": " ⏰", "excited": " ⚡", "synonyms": ["due", "timeline", "cutoff"]},
    "friends": {"default": " 👯", "funny": " 👯‍♂️", "sarcastic": " 🤝", "motivational": " 👬", "cute": " 👭", "excited": " 👯", "synonyms": ["buddies", "pals", "mates"]},
    "success": {"default": " 🏆", "funny": " 🎉", "sarcastic": " 🥳", "motivational": " 💯", "cute": " 💎", "excited": " 🥇", "synonyms": ["victory", "achievement", "triumph"]},
    "thankful": {"default": " 🙏", "funny": " 🙌", "sarcastic": " 😏", "motivational": " 👏", "cute": " ❤️", "excited": " 🙏", "synonyms": ["grateful", "appreciative", "thank"]},
    "party": {"default": " 🎉", "funny": " 🎈", "sarcastic": " 🥂", "motivational": " 💥", "cute": " 🎊", "excited": " 🍾", "synonyms": ["celebration", "festivity", "bash"]},
    "grateful": {"default": " 🙏", "funny": " 🙇", "sarcastic": " 😉", "motivational": " 🤝", "cute": " 🦋", "excited": " 🌟", "synonyms": ["thankful", "appreciative", "obliged"]},
    "adventure": {"default": " 🌍", "funny": " 🚶", "sarcastic": " 🏞️", "motivational": " 🗺️", "cute": " 🎒", "excited": " 🌄", "synonyms": ["journey", "expedition", "quest"]},
    "travel": {"default": " ✈️", "funny": " 🚂", "sarcastic": " 🛳️", "motivational": " 🚗", "cute": " 🏖️", "excited": " 🗺️", "synonyms": ["trip", "voyage", "tour"]},
    "nature": {"default": " 🌿", "funny": " 🌴", "sarcastic": " 🌳", "motivational": " 🌸", "cute": " 🌺", "excited": " 🌻", "synonyms": ["outdoors", "wilderness", "scenery"]}
}

def emojify_text(text, mood="default", intensity=2, use_sentiment=True):
    if not text or not isinstance(text, str):
        return "No valid text provided"
    
    # Split text into sentences while preserving punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    result_sentences = []
    
    # Compute paragraph-level sentiment
    paragraph_blob = TextBlob(text)
    paragraph_sentiment = paragraph_blob.sentiment.polarity
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Tokenize and get POS tags
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        result_tokens = []
        blob = TextBlob(sentence)
        emoji_count = 0
        
        for token, pos in pos_tags:
            # Only add emojis for nouns (NN*), verbs (VB*), and adjectives (JJ*)
            if re.match(r'\w+', token.lower()) and pos.startswith(('NN', 'VB', 'JJ')):
                clean = token.lower()
                matched_key = clean
                
                # Check for synonyms
                for key, data in emoji_dict.items():
                    if clean in data.get("synonyms", []):
                        matched_key = key
                        break
                
                if matched_key in emoji_dict and (emoji_count < intensity or intensity == 3):
                    emoji = emoji_dict[matched_key].get(mood, emoji_dict[matched_key]["default"])
                    result_tokens.append(f"{token}{emoji}")
                    emoji_count += 1
                else:
                    result_tokens.append(token)
            else:
                # Preserve punctuation and other tokens
                result_tokens.append(token)
        
        # Join tokens back into sentence
        emojified_sentence = ' '.join(result_tokens)
        
        # Add sentiment-based emoji if enabled and within intensity limit
        if use_sentiment and emoji_count < intensity:
            sentiment = blob.sentiment.polarity
            # Adjust sentiment based on paragraph context
            if paragraph_sentiment < -0.2 and sentiment > 0:
                sentiment = -0.1  # Tone down positive sentiment in negative context
            elif paragraph_sentiment > 0.2 and sentiment < 0:
                sentiment = 0.1   # Tone down negative sentiment in positive context
                
            if sentiment > 0.3:
                emojified_sentence += emoji_dict['happy'].get(mood, emoji_dict['happy']['default'])
            elif sentiment < -0.3:
                emojified_sentence += emoji_dict['sad'].get(mood, emoji_dict['sad']['default'])
            
        result_sentences.append(emojified_sentence)
    
    # Join sentences with proper spacing
    return '\n\n'.join(result_sentences)
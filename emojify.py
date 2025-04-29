import nltk
from textblob import TextBlob
import re
import os

# Set NLTK data path to a writable directory
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data
try:
    nltk.download("punkt", download_dir=nltk_data_dir, quiet=True)
    nltk.download("punkt_tab", download_dir=nltk_data_dir, quiet=True)
    nltk.download("averaged_perceptron_tagger_eng", download_dir=nltk_data_dir, quiet=True)
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
    
    # Use NLTK's sentence tokenizer and split on conjunctions like "but"
    initial_sentences = nltk.sent_tokenize(text.strip())
    sentences = []
    for sent in initial_sentences:
        # Split on "but" and commas for finer granularity
        split_sentences = re.split(r'\s*(?:but|and|,)\s*', sent)
        sentences.extend([s.strip() for s in split_sentences if s.strip()])
    
    print(f"Split Sentences: {sentences}")
    result_sentences = []
    
    # Expanded list of negative words
    negative_words = [
        'stressful', 'bad', 'sad', 'terrible', 'awful', 'horrible', 'tired',
        'exhausted', 'angry', 'frustrated', 'confusing', 'hurt', 'painful',
        'difficult', 'tough', 'annoying', 'boring', 'disappointing'
    ]
    
    # List of positive words to force positive sentiment
    positive_words = [
        'happy', 'love', 'excited', 'free', 'success', 'thankful', 'grateful',
        'party', 'joyful', 'cheerful', 'glad', 'adore', 'cherish', 'affection',
        'thrilled', 'eager', 'enthusiastic'
    ]
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Tokenize and get POS tags
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        result_tokens = []
        blob = TextBlob(sentence)
        emoji_count = 0
        
        # Negation detection for the sentence
        negation_words = ['not', "n't", 'never', 'no']
        has_negation = any(word.lower() in sentence.lower() for word in negation_words)
        
        # Check for double negation (e.g., "not unhappy")
        is_double_negation = False
        for i, token in enumerate(tokens):
            if token.lower() in negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1].lower()
                if next_token.startswith('un') and next_token in ['unhappy', 'unpleasant', 'unsatisfied']:
                    is_double_negation = True
                    break
        
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
                
                # Skip positive emojis if single negation and positive key
                # Skip negative emojis if double negation and negative key
                if matched_key in emoji_dict and (emoji_count < intensity or intensity == 3):
                    if has_negation and not is_double_negation and matched_key in ['happy', 'love', 'excited', 'free', 'success', 'thankful', 'grateful', 'party']:
                        result_tokens.append(token)
                    elif is_double_negation and matched_key in ['sad', 'angry', 'tired', 'bored', 'confused']:
                        result_tokens.append(token)
                    else:
                        emoji = emoji_dict[matched_key].get(mood, emoji_dict[matched_key]["default"])
                        result_tokens.append(f"{token}{emoji}")
                        emoji_count += 1
                        print(f"Word-Level: Token: {token}, Matched Key: {matched_key}, Emoji: {emoji}, Double Negation: {is_double_negation}")
                else:
                    result_tokens.append(token)
            else:
                result_tokens.append(token)
        
        # Join tokens back into sentence
        emojified_sentence = ' '.join(result_tokens)
        
        # Add sentiment-based emoji if enabled and within intensity limit
        if use_sentiment and emoji_count < intensity:
            sentiment = blob.sentiment.polarity
            
            # Handle double negation
            if is_double_negation and sentiment < 0:
                sentiment = -sentiment
            # Handle single negation
            elif has_negation and not is_double_negation and sentiment > 0:
                sentiment = -sentiment
            
            # Force negative sentiment if negative words are present
            if any(word.lower() in sentence.lower() for word in negative_words):
                sentiment = min(sentiment, -0.3)
            
            # Force positive sentiment if positive words are present and sentiment is neutral or slightly positive
            if any(word.lower() in sentence.lower() for word in positive_words) and sentiment >= 0.5:
                sentiment = max(sentiment, 0.6)  # Bump to ensure positive emoji
            
            # Debug print for sentiment analysis
            print(f"Sentence: {sentence}, Negative Words: {[word for word in negative_words if word.lower() in sentence.lower()]}, Positive Words: {[word for word in positive_words if word.lower() in sentence.lower()]}, Has Negation: {has_negation}, Double Negation: {is_double_negation}, Sentiment: {sentiment}")
            
            if sentiment > 0.5:  # Keep strict positive threshold
                emojified_sentence += emoji_dict['happy'].get(mood, emoji_dict['happy']['default'])
            elif sentiment < -0.01:
                emojified_sentence += emoji_dict['sad'].get(mood, emoji_dict['sad']['default'])
            else:
                print(f"Neutral sentiment skipped: {sentiment}")
            
        result_sentences.append(emojified_sentence)
    
    # Join sentences with proper spacing
    return '\n\n'.join(result_sentences)
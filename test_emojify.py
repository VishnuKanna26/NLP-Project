import unittest
from emojify import emojify_text

class TestEmojifyText(unittest.TestCase):
    def test_positive_sentiment_cute(self):
        input_text = "I am very happy today!"
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("🥰", result, "Positive sentiment should include happy emoji (cute mood)")
        self.assertNotIn("😞", result, "Positive sentiment should not include sad emoji")

    def test_negative_sentiment_cute(self):
        input_text = "I am not feeling good."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("😞", result, "Negative sentiment should include sad emoji")
        self.assertNotIn("🥰", result, "Negative sentiment should not include happy emoji")

    def test_negation_handling_cute(self):
        input_text = "I am not happy today."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("😞", result, "Negation should result in sad emoji")
        self.assertNotIn("🥰", result, "Negation should not include happy emoji")

    def test_neutral_sentiment_cute(self):
        input_text = "I am going to the park."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertNotIn("🥰", result, "Neutral sentiment should not include happy emoji")
        self.assertNotIn("😞", result, "Neutral sentiment should not include sad emoji")

    def test_mixed_sentiment_cute(self):
        input_text = "I am happy but exams are stressful."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("🥰", result, "First sentence should include happy emoji")
        self.assertIn("😞", result, "Second sentence should include sad emoji")

    def test_double_negation_cute(self):
        input_text = "I am not unhappy today."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertNotIn("😞", result, "Double negation should not include sad emoji")

    def test_short_negative_cute(self):
        input_text = "This is awful."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("😞", result, "Short negative sentence should include sad emoji")
        self.assertNotIn("🥰", result, "Short negative sentence should not include happy emoji")

    def test_ambiguous_sentiment_cute(self):
        input_text = "The movie was okay but confusing."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("😞", result, "Ambiguous sentence with negative word should include sad emoji")
        self.assertNotIn("🥰", result, "Ambiguous sentence should not include happy emoji")

    def test_complex_sentence_cute(self):
        input_text = "I love dancing, but my feet hurt and exams are tomorrow."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertIn("🥰", result, "Complex sentence should include happy emoji for positive part")
        self.assertIn("😞", result, "Complex sentence should include sad emoji for negative part")

    def test_no_words_matched_cute(self):
        input_text = "The sky is blue."
        result = emojify_text(input_text, mood="cute", intensity=2, use_sentiment=True)
        self.assertNotIn("🥰", result, "Neutral sentence with no matched words should not include happy emoji")
        self.assertNotIn("😞", result, "Neutral sentence with no matched words should not include sad emoji")

    def test_high_intensity_cute(self):
        input_text = "I am super happy and excited!"
        result = emojify_text(input_text, mood="cute", intensity=3, use_sentiment=True)
        self.assertIn("🥰", result, "High intensity positive sentence should include happy emoji")
        self.assertIn("🤩", result, "High intensity positive sentence should include excited emoji")
        self.assertNotIn("😞", result, "High intensity positive sentence should not include sad emoji")

    def test_positive_sentiment_funny(self):
        input_text = "I am very happy today!"
        result = emojify_text(input_text, mood="funny", intensity=2, use_sentiment=True)
        self.assertIn("😂", result, "Positive sentiment should include happy emoji (funny mood)")
        self.assertNotIn("😭", result, "Positive sentiment should not include sad emoji")

    def test_negative_sentiment_sarcastic(self):
        input_text = "I am not feeling good."
        result = emojify_text(input_text, mood="sarcastic", intensity=2, use_sentiment=True)
        self.assertIn("😑", result, "Negative sentiment should include sad emoji (sarcastic mood)")
        self.assertNotIn("🙄", result, "Negative sentiment should not include happy emoji")

    def test_double_negation_funny(self):
        input_text = "I am not unhappy today."
        result = emojify_text(input_text, mood="funny", intensity=2, use_sentiment=True)
        self.assertNotIn("😭", result, "Double negation should not include sad emoji")

    # New tests for default mood
    def test_positive_sentiment_default(self):
        input_text = "I am very happy today!"
        result = emojify_text(input_text, mood="default", intensity=2, use_sentiment=True)
        self.assertIn("😊", result, "Positive sentiment should include happy emoji (default mood)")
        self.assertNotIn("😢", result, "Positive sentiment should not include sad emoji")

    def test_negative_sentiment_default(self):
        input_text = "This is awful."
        result = emojify_text(input_text, mood="default", intensity=2, use_sentiment=True)
        self.assertIn("😢", result, "Negative sentiment should include sad emoji (default mood)")
        self.assertNotIn("😊", result, "Negative sentiment should not include happy emoji")

    def test_complex_sentence_default(self):
        input_text = "I love dancing, but my feet hurt."
        result = emojify_text(input_text, mood="default", intensity=2, use_sentiment=True)
        self.assertIn("😊", result, "Complex sentence should include happy emoji for positive part")
        self.assertIn("😢", result, "Complex sentence should include sad emoji for negative part")

    # New tests for motivational mood
    def test_positive_sentiment_motivational(self):
        input_text = "I am very happy today!"
        result = emojify_text(input_text, mood="motivational", intensity=2, use_sentiment=True)
        self.assertIn("💪", result, "Positive sentiment should include happy emoji (motivational mood)")
        self.assertNotIn("😔", result, "Positive sentiment should not include sad emoji")

    def test_negative_sentiment_motivational(self):
        input_text = "This is awful."
        result = emojify_text(input_text, mood="motivational", intensity=2, use_sentiment=True)
        self.assertIn("😔", result, "Negative sentiment should include sad emoji (motivational mood)")
        self.assertNotIn("💪", result, "Negative sentiment should not include happy emoji")

    def test_complex_sentence_motivational(self):
        input_text = "I love dancing, but my feet hurt."
        result = emojify_text(input_text, mood="motivational", intensity=2, use_sentiment=True)
        self.assertIn("💪", result, "Complex sentence should include happy emoji for positive part")
        self.assertIn("😔", result, "Complex sentence should include sad emoji for negative part")

    # New tests for excited mood
    def test_positive_sentiment_excited(self):
        input_text = "I am very happy today!"
        result = emojify_text(input_text, mood="excited", intensity=2, use_sentiment=True)
        self.assertIn("😆", result, "Positive sentiment should include happy emoji (excited mood)")
        self.assertNotIn("😩", result, "Positive sentiment should not include sad emoji")

    def test_negative_sentiment_excited(self):
        input_text = "This is awful."
        result = emojify_text(input_text, mood="excited", intensity=2, use_sentiment=True)
        self.assertIn("😩", result, "Negative sentiment should include sad emoji (excited mood)")
        self.assertNotIn("😆", result, "Negative sentiment should not include happy emoji")

    def test_complex_sentence_excited(self):
        input_text = "I love dancing, but my feet hurt."
        result = emojify_text(input_text, mood="excited", intensity=2, use_sentiment=True)
        self.assertIn("😆", result, "Complex sentence should include happy emoji for positive part")
        self.assertIn("😩", result, "Complex sentence should include sad emoji for negative part")

if __name__ == '__main__':
    unittest.main()
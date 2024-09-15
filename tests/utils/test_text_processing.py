# Copyright 2024 fukuro-kun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from src.backend.text_processor import detect_language, words_to_digits, digits_to_words

class TestTextProcessing(unittest.TestCase):

    def test_detect_language(self):
        self.assertEqual(detect_language("Das ist ein deutscher Satz."), 'de')
        self.assertEqual(detect_language("This is an English sentence."), 'en')
        self.assertEqual(detect_language("Ein Satz mit both languages."), 'de')

    def test_words_to_digits_german(self):
        self.assertEqual(words_to_digits("Ich habe dreiundzwanzig Äpfel."), "Ich habe 23 Äpfel.")
        self.assertEqual(words_to_digits("eins zwei drei"), "1 2 3")
        self.assertEqual(words_to_digits("Das ist ein Test."), "Das ist ein Test.")
        self.assertEqual(words_to_digits("einundzwanzig"), "21")
        self.assertEqual(words_to_digits("vierhundertsechsundfünfzig"), "456")
        self.assertEqual(words_to_digits("zweitausend"), "2000")
        self.assertEqual(words_to_digits("zwanzigtausend"), "20000")
        self.assertEqual(words_to_digits("einundzwanzigtausend"), "21000")
        self.assertEqual(words_to_digits("zweihunderttausend"), "200000")
        self.assertEqual(words_to_digits("dreihundertfünfundvierzigtausend"), "345000")
        self.assertEqual(words_to_digits("eine Million zweihunderttausenddreihundertfünfundvierzig"), "1200345")
        self.assertEqual(words_to_digits("zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig"), "2345678")

    def test_words_to_digits_english(self):
        self.assertEqual(words_to_digits("I have twenty-three apples."), "I have 23 apples.")
        self.assertEqual(words_to_digits("one two three"), "1 2 3")
        self.assertEqual(words_to_digits("This is a test."), "This is a test.")
        self.assertEqual(words_to_digits("twenty-one"), "21")
        self.assertEqual(words_to_digits("four hundred fifty-six"), "456")

    def test_digits_to_words_german(self):
        self.assertEqual(digits_to_words("Ich habe 23 Äpfel.", 'de'), "Ich habe dreiundzwanzig Äpfel.")
        self.assertEqual(digits_to_words("1 2 3", 'de'), "ein zwei drei")
        self.assertEqual(digits_to_words("456", 'de'), "vierhundertsechsundfünfzig")
        self.assertEqual(digits_to_words("2000", 'de'), "zweitausend")
        self.assertEqual(digits_to_words("20000", 'de'), "zwanzigtausend")
        self.assertEqual(digits_to_words("21000", 'de'), "einundzwanzigtausend")
        self.assertEqual(digits_to_words("200000", 'de'), "zweihunderttausend")
        self.assertEqual(digits_to_words("345000", 'de'), "dreihundertfünfundvierzigtausend")
        self.assertEqual(digits_to_words("1200345", 'de'), "eine Million zweihundertausenddreihundertfünfundvierzig")
        self.assertEqual(digits_to_words("2345678", 'de'), "zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig")

    def test_digits_to_words_english(self):
        self.assertEqual(digits_to_words("I have 23 apples.", 'en'), "I have twenty-three apples.")
        self.assertEqual(digits_to_words("1 2 3", 'en'), "one two three")
        self.assertEqual(digits_to_words("456", 'en'), "four hundred fifty-six")

    def test_mixed_conversion(self):
        original = "Ich habe 5 Äpfel und twenty Birnen."
        to_digits = words_to_digits(original)
        self.assertEqual(to_digits, "Ich habe 5 Äpfel und 20 Birnen.")
        back_to_words = digits_to_words(to_digits, 'de')
        self.assertEqual(back_to_words, "Ich habe fünf Äpfel und zwanzig Birnen.")

if __name__ == '__main__':
    unittest.main()

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
from termcolor import colored

class TestTextProcessing(unittest.TestCase):

    def test_detect_language(self):
        self.assertEqual(detect_language("Das ist ein deutscher Satz."), 'de')
        self.assertEqual(detect_language("This is an English sentence."), 'en')
        self.assertEqual(detect_language("Ein Satz mit both languages."), 'de')

    def test_words_to_digits_german(self):
        test_cases = [
            ("Ich habe dreiundzwanzig Äpfel.", "Ich habe 23 Äpfel."),
            ("eins zwei drei", "1 2 3"),
            ("Das ist ein Test.", "Das ist ein Test."),
            ("einundzwanzig", "21"),
            ("vierhundertsechsundfünfzig", "456"),
            ("zweitausend", "2000"),
            ("zwanzigtausend", "20000"),
            ("einundzwanzigtausend", "21000"),
            ("zweihunderttausend", "200000"),
            ("dreihundertfünfundvierzigtausend", "345000"),
            ("dreihundertfünfundvierzigtausendsechshundertachtundsiebzig", "345678"),
            ("eine Million zweihunderttausenddreihundertfünfundvierzig", "1200345"),
            ("zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig", "2345678")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = words_to_digits(input_text)
                self.assertEqual(result, expected_output)
                print(f"Input: {input_text}")
                print(f"Expected: {expected_output}")
                if result == expected_output:
                    print(colored(f"Result: {result}", "green"))
                else:
                    print(colored(f"Result: {result}", "red"))
                print()

    def test_digits_to_words_german(self):
        test_cases = [
            ("Ich habe 23 Äpfel.", "Ich habe dreiundzwanzig Äpfel."),
            ("1 2 3", "eins zwei drei"),
            ("456", "vierhundertsechsundfünfzig"),
            ("2000", "zweitausend"),
            ("2001", "zweitausendeins"),
            ("20000", "zwanzigtausend"),
            ("20001", "zwanzigtausendeins"),
            ("21000", "einundzwanzigtausend"),
            ("200000", "zweihunderttausend"),
            ("345000", "dreihundertfünfundvierzigtausend"),
            ("345678", "dreihundertfünfundvierzigtausendsechshundertachtundsiebzig"),
            ("1200345", "eine Million zweihunderttausenddreihundertfünfundvierzig"),
            ("2345678", "zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = digits_to_words(input_text, 'de')
                self.assertEqual(result, expected_output)
                print(f"Input: {input_text}")
                print(f"Expected: {expected_output}")
                if result == expected_output:
                    print(colored(f"Result: {result}", "green"))
                else:
                    print(colored(f"Result: {result}", "red"))
                print()

    def test_words_to_digits_english(self):
        self.assertEqual(words_to_digits("I have twenty-three apples."), "I have 23 apples.")
        self.assertEqual(words_to_digits("one two three"), "1 2 3")
        self.assertEqual(words_to_digits("This is a test."), "This is a test.")
        self.assertEqual(words_to_digits("twenty-one"), "21")
        self.assertEqual(words_to_digits("four hundred fifty-six"), "456")

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

# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from src.backend.text_processor import TextProcessor, parse_german_number, words_to_digits, digits_to_words
from termcolor import colored

class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessor()

    def test_parse_german_number(self):
        test_cases = [
            ("dreiundzwanzig", 23),
            ("siebenhundertachtundzwanzig", 728),
            ("eintausendneunhundertneunundneunzig", 1999),
            ("zweihundertzehntausendvier", 210004),
            ("zweiundvierzigtausendzehn", 42010),
            ("eine Million zweihunderttausenddreihundertfünfundvierzig", 1200345),
            ("zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig", 2345678),
            ("eine Milliarde zweihundertmillionen dreihunderttausend", 1200300000),
            ("eins", 1),
            ("einundzwanzig", 21),
            ("zweiundzwanzigtausenddreihundertvierundfünfzig", 22354),
            ("neunundneunzigtausendneunhundertneunundneunzig", 99999),
            ("eine Million", 1000000),
            ("zweitausendeinundzwanzig", 2021),
            ("dreitausendsiebenhunderteinundzwanzig", 3721),
            ("neunzehnhundertvierundachtzig", 1984),
            ("zweitausendachtzehn", 2018),
            ("einhundertundeins", 101),
            ("tausendundeins", 1001),
            ("eine Milliarde eins", 1000000001),
            ("zweihundertmillionen", 200000000),
            ("neunhundertneunundneunzigtausendneunhundertneunundneunzig", 999999),
            ("eine Million undeins", 1000001),
            ("zweiundzwanzig Millionen dreihundertvierundfünfzigtausendsechshundertachtundsiebzig", 22354678),
            ("dreizehnmillionenzweihundertvierunddreißigtausendfünfhundertsiebenundsechzig", 13234567),
            ("vierundvierzig Milliarden siebenhundertdreiundzwanzig Millionen neunhunderteinundfünfzigtausendsechshundertachtundsiebzig", 44723951678),
        ]

        for words, expected in test_cases:
            with self.subTest(words=words, expected=expected):
                result, _ = parse_german_number(words)
                self.assertEqual(result, expected)
                print(f"Input: {words}")
                print(f"Expected: {expected}")
                if result == expected:
                    print(colored(f"Result: {result}", "green"))
                else:
                    print(colored(f"Result: {result}", "red"))
                print()

    def test_words_to_digits(self):
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

    def test_digits_to_words(self):
        test_cases = [
            ("Ich habe 23 Äpfel.", "Ich habe dreiundzwanzig Äpfel."),
            ("1 2 3", "eins zwei drei"),
            ("456", "vierhundertsechsundfünfzig"),
            ("2000", "zweitausend"),
            ("2001", "zweitausendundeins"),
            ("20000", "zwanzigtausend"),
            ("20001", "zwanzigtausendundeins"),
            ("21000", "einundzwanzigtausend"),
            ("200000", "zweihunderttausend"),
            ("345000", "dreihundertfünfundvierzigtausend"),
            ("345678", "dreihundertfünfundvierzigtausendsechshundertachtundsiebzig"),
            ("1200345", "eine Million zweihunderttausenddreihundertfünfundvierzig"),
            ("2345678", "zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = digits_to_words(input_text)
                self.assertEqual(result, expected_output)
                print(f"Input: {input_text}")
                print(f"Expected: {expected_output}")
                if result == expected_output:
                    print(colored(f"Result: {result}", "green"))
                else:
                    print(colored(f"Result: {result}", "red"))
                print()

    def test_text_processor_process_text(self):
        test_cases = [
            ("Ich habe dreiundzwanzig Äpfel und 45 Birnen.", "Ich habe 23 Äpfel und 45 Birnen."),
            ("1 2 3 vier fünf sechs", "1 2 3 4 5 6"),
            ("Das sind einhundertdreiundzwanzig Euro und 45 Cent.", "Das sind 123 Euro und 45 Cent.")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = self.text_processor.process_text(input_text, 'de')
                self.assertEqual(result, expected_output)
                print(f"Input: {input_text}")
                print(f"Expected: {expected_output}")
                if result == expected_output:
                    print(colored(f"Result: {result}", "green"))
                else:
                    print(colored(f"Result: {result}", "red"))
                print()

if __name__ == '__main__':
    unittest.main()

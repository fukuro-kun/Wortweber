import unittest
from src.backend.text_processor import TextProcessor, parse_german_number, words_to_digits, digits_to_words

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
            ("einhunderteins", 101),
            ("tausendeins", 1001),
            ("eine Milliarde eins", 1000000001),
            ("zweihundertmillionen", 200000000),
            ("neunhundertneunundneunzigtausendneunhundertneunundneunzig", 999999),
            ("eine Million eine", 1000001),
            ("zweiundzwanzig Millionen dreihundertvierundfünfzigtausendsechshundertachtundsiebzig", 22354678),
            ("dreizehnmillionenzweihundertvierunddreißigtausendfünfhundertsiebenundsechzig", 13234567),
            ("vierundvierzig Milliarden siebenhundertdreiundzwanzig Millionen neunhunderteinundfünfzigtausendsechshundertachtundsiebzig", 44723951678),
        ]

        for words, expected in test_cases:
            with self.subTest(words=words, expected=expected):
                result = parse_german_number(words)
                self.assertEqual(result, expected)

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

    def test_digits_to_words(self):
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
                result = digits_to_words(input_text)
                self.assertEqual(result, expected_output)

    def test_text_processor_process_text(self):
        test_cases = [
            ("Ich habe dreiundzwanzig Äpfel und 45 Birnen.", "Ich habe 23 Äpfel und 45 Birnen."),
            ("1 2 3 vier fünf sechs", "1 2 3 4 5 6"),
            ("Das sind einhundertdreiundzwanzig Euro und 45 Cent.", "Das sind 123 Euro und 45 Cent.")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = self.text_processor.process_text(input_text)
                self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

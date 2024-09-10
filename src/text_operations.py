# Wortweber/src/text_operations.py

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

# Diese Datei verwendet die folgenden Bibliotheken:
# num2words: GNU Lesser General Public License v2.1 (LGPL-2.1)
# word2number: MIT License

import re
from num2words import num2words
from word2number import w2n

def detect_language(text):
    """Erkennt die Sprache des Textes basierend auf spezifischen Wörtern."""
    german_words = set(['und', 'der', 'die', 'das', 'ein', 'eine', 'ist', 'sind', 'haben', 'hatte'])
    english_words = set(['and', 'the', 'a', 'an', 'is', 'are', 'have', 'had'])

    words = set(text.lower().split())
    german_count = len(words.intersection(german_words))
    english_count = len(words.intersection(english_words))

    return 'de' if german_count > english_count else 'en'

def words_to_digits(text):
    """Wandelt Zahlwörter in einem Text in Ziffern um."""
    language = detect_language(text)
    words = text.split()
    result = []
    i = 0
    while i < len(words):
        try:
            # Versuche, das Wort oder die Wortgruppe in eine Zahl umzuwandeln
            number = w2n.word_to_num(words[i])
            result.append(str(number))
            i += 1
        except ValueError:
            # Wenn es keine Zahl ist, füge das Wort unverändert hinzu
            result.append(words[i])
            i += 1
    return ' '.join(result)

def digits_to_words(text):
    """Wandelt Ziffern in einem Text in Zahlwörter um."""
    language = detect_language(text)

    def replace_number(match):
        number = int(match.group())
        return num2words(number, lang=language)

    return re.sub(r'\d+', replace_number, text)

# Testfunktion
if __name__ == "__main__":
    test_texts = [
        "Ich habe dreiundzwanzig Äpfel und vierhundertsechsundfünfzig Birnen.",
        "I have twenty-three apples and four hundred fifty-six pears."
    ]

    for test_text in test_texts:
        print("Original:", test_text)
        digits_text = words_to_digits(test_text)
        print("Zahlwörter zu Ziffern:", digits_text)
        words_text = digits_to_words(digits_text)
        print("Ziffern zu Zahlwörtern:", words_text)
        print()

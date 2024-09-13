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

# src/backend/text_processor.py

import re

def detect_language(text):
    """
    Erkennt die Sprache des Textes basierend auf spezifischen Wörtern.

    :param text: Der zu analysierende Text
    :return: 'de' für Deutsch oder 'en' für Englisch

    Diese Funktion verwendet eine einfache Heuristik, indem sie zählt, wie viele
    typische deutsche bzw. englische Wörter im Text vorkommen.
    """
    german_words = set(['und', 'der', 'die', 'das', 'ein', 'eine', 'ist', 'sind', 'haben', 'hatte'])
    english_words = set(['and', 'the', 'a', 'an', 'is', 'are', 'have', 'had'])

    words = set(text.lower().split())
    german_count = len(words.intersection(german_words))
    english_count = len(words.intersection(english_words))

    return 'de' if german_count > english_count else 'en'

# Globale Wörterbücher für Zahlen
GERMAN_NUMBER_DICT = {
    'null': '0', 'ein': '1', 'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5',
    'sechs': '6', 'sieben': '7', 'acht': '8', 'neun': '9', 'zehn': '10', 'elf': '11', 'zwölf': '12',
    'dreizehn': '13', 'vierzehn': '14', 'fünfzehn': '15', 'sechzehn': '16', 'siebzehn': '17',
    'achtzehn': '18', 'neunzehn': '19', 'zwanzig': '20', 'dreißig': '30', 'vierzig': '40',
    'fünfzig': '50', 'sechzig': '60', 'siebzig': '70', 'achtzig': '80', 'neunzig': '90',
    'hundert': '100', 'tausend': '1000', 'million': '1000000', 'milliarde': '1000000000'
}

ENGLISH_NUMBER_DICT = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10'
}

def words_to_digits(text):
    """
    Wandelt Zahlwörter in einem Text in Ziffern um.

    :param text: Der zu verarbeitende Text
    :return: Der Text mit umgewandelten Zahlwörtern

    Diese Funktion erkennt zunächst die Sprache des Textes und wendet dann
    das entsprechende Wörterbuch an, um Zahlwörter in Ziffern umzuwandeln.
    """
    language = detect_language(text)
    if language == 'de':
        number_dict = GERMAN_NUMBER_DICT
    else:
        number_dict = ENGLISH_NUMBER_DICT

    pattern = r'\b(' + '|'.join(number_dict.keys()) + r')\b'
    return re.sub(pattern, lambda m: number_dict[m.group().lower()], text, flags=re.IGNORECASE)

def digits_to_words(text):
    """
    Wandelt Ziffern in einem Text in Zahlwörter um.

    :param text: Der zu verarbeitende Text
    :return: Der Text mit umgewandelten Ziffern

    Diese Funktion erkennt zunächst die Sprache des Textes und wendet dann
    das entsprechende umgekehrte Wörterbuch an, um Ziffern in Zahlwörter umzuwandeln.
    """
    language = detect_language(text)

    if language == 'de':
        number_dict = {v: k for k, v in GERMAN_NUMBER_DICT.items() if v.isdigit()}
    else:
        number_dict = {v: k for k, v in ENGLISH_NUMBER_DICT.items()}

    pattern = r'\b\d+\b'
    return re.sub(pattern, lambda m: number_dict.get(m.group(), m.group()), text)

# Testfunktion
if __name__ == "__main__":
    test_texts = [
        "Ich habe dreiundzwanzig Äpfel und vierhundertsechsundfünfzig Birnen.",
        "I have twenty-three apples and four hundred fifty-six pears.",
        "eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn. Das ist ein kleiner Test.",
        "Das ist ein kleiner Test. 12, 23, 45, 4567",
        "Das ist ein kleiner Test. zwölf, dreiundzwanzig, fünfundvierzig, viertausendfünfhundertsiebenundsechzig"
    ]

    for test_text in test_texts:
        print("Original:", test_text)
        digits_text = words_to_digits(test_text)
        print("Zahlwörter zu Ziffern:", digits_text)
        words_text = digits_to_words(digits_text)
        print("Ziffern zu Zahlwörtern:", words_text)
        print()

# Zusätzliche Erklärungen:

# 1. Spracherkennung:
#    Die `detect_language` Funktion verwendet eine einfache, aber effektive Methode zur Spracherkennung.
#    Sie basiert auf der Annahme, dass bestimmte häufig vorkommende Wörter charakteristisch für eine Sprache sind.
#    Diese Methode ist nicht perfekt, aber ausreichend für die Zwecke dieser Anwendung.

# 2. Reguläre Ausdrücke:
#    Die Funktionen `words_to_digits` und `digits_to_words` verwenden reguläre Ausdrücke (re.sub) für die Textumwandlung.
#    Der Ausdruck r'\b(' + '|'.join(number_dict.keys()) + r')\b' erstellt ein Muster, das alle Schlüssel des Wörterbuchs als Wörter matcht.
#    r'\b\d+\b' matcht alleinstehende Ziffernfolgen.

# 3. Lambda-Funktionen:
#    In den re.sub Aufrufen werden Lambda-Funktionen verwendet, um die eigentliche Ersetzung durchzuführen.
#    Diese anonymen Funktionen erlauben eine kompakte Schreibweise für einfache Operationen.

# 4. Wörterbuch-Umkehrung:
#    In `digits_to_words` wird das Wörterbuch umgekehrt, um von Ziffern auf Wörter zu mappen.
#    Die Verwendung von .isdigit() stellt sicher, dass nur numerische Schlüssel berücksichtigt werden.

# 5. Testfunktion:
#    Der __main__ Block enthält eine Testfunktion, die die Funktionalität der Textverarbeitung demonstriert.
#    Dies ist nützlich für schnelle Tests und zur Veranschaulichung der Funktionsweise.

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

import re
from termcolor import colored

def detect_language(text):
    """
    Erkennt die Sprache des Textes basierend auf spezifischen Wörtern.

    :param text: Der zu analysierende Text
    :return: 'de' für Deutsch oder 'en' für Englisch
    """
    german_words = set(['und', 'der', 'die', 'das', 'ein', 'eine', 'ist', 'sind', 'haben', 'hatte', 'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'sie'])
    english_words = set(['and', 'the', 'a', 'an', 'is', 'are', 'have', 'had', 'I', 'you', 'he', 'she', 'it', 'we', 'they'])

    words = set(re.findall(r'\b\w+\b', text.lower()))
    german_count = len(words.intersection(german_words))
    english_count = len(words.intersection(english_words))

    return 'de' if german_count >= english_count else 'en'

# Erweiterte Wörterbücher für Zahlen
GERMAN_NUMBER_DICT = {
    'null': 0, 'ein': 1, 'eine': 1, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5,
    'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12,
    'dreizehn': 13, 'vierzehn': 14, 'fünfzehn': 15, 'sechzehn': 16, 'siebzehn': 17,
    'achtzehn': 18, 'neunzehn': 19, 'zwanzig': 20, 'dreißig': 30, 'vierzig': 40,
    'fünfzig': 50, 'sechzig': 60, 'siebzig': 70, 'achtzig': 80, 'neunzig': 90,
    'hundert': 100, 'tausend': 1000, 'million': 1000000, 'millionen': 1000000, 'milliarde': 1000000000
}

ENGLISH_NUMBER_DICT = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
    'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,
    'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
    'hundred': 100, 'thousand': 1000, 'million': 1000000, 'billion': 1000000000
}

def parse_german_number(words):
    total = 0
    current = 0
    for word in words:
        if word == 'und':
            continue
        if word in GERMAN_NUMBER_DICT:
            value = GERMAN_NUMBER_DICT[word]
            if value == 1 and current == 0:
                current = 1
            elif value < 100:
                current += value
            elif value == 100:
                current = current * 100 if current != 0 else 100
            elif value >= 1000:
                total += (current if current != 0 else 1) * value
                current = 0
        else:
            # DEUTSCH: Behandlung zusammengesetzter Wörter
            for key, val in sorted(GERMAN_NUMBER_DICT.items(), key=lambda x: len(x[0]), reverse=True):
                if word.endswith(key):
                    prefix = word[:-len(key)]
                    if prefix in GERMAN_NUMBER_DICT:
                        if val >= 1000:
                            total += GERMAN_NUMBER_DICT[prefix] * val
                        else:
                            current += GERMAN_NUMBER_DICT[prefix] * val
                    break
    return total + current

def parse_english_number(words):
    total = 0
    current = 0
    for word in words:
        if word == 'and':
            continue
        elif word in ENGLISH_NUMBER_DICT:
            value = ENGLISH_NUMBER_DICT[word]
            if value == 100:
                current = current * 100 if current != 0 else 100
            elif value >= 1000:
                total += current * value
                current = 0
            else:
                current += value
    return total + current

def words_to_digits(text):
    """
    Wandelt Zahlwörter in einem Text in Ziffern um.

    :param text: Der zu verarbeitende Text
    :return: Der Text mit umgewandelten Zahlwörtern
    """
    language = detect_language(text)
    number_dict = GERMAN_NUMBER_DICT if language == 'de' else ENGLISH_NUMBER_DICT

    def replace_number(match):
        words = match.group(0).lower().replace('-', ' ').split()
        # DEUTSCH: Behandlung von einzeln stehenden Wörtern wie "ein"
        if len(words) == 1 and words[0] in ['ein', 'eine']:
            return match.group(0)
        if language == 'de':
            # DEUTSCH: Behandlung von "eine Million" und ähnlichen Fällen
            if words[0] == 'eine' and len(words) > 1 and words[1] in ['million', 'milliarde']:
                words[0] = 'ein'
            number = parse_german_number(words)
        else:
            number = parse_english_number(words)
        return str(number) if number is not None else match.group(0)

    # Muster für zusammengesetzte Zahlen
    pattern = r'\b(?:(?:' + '|'.join(re.escape(k) for k in number_dict.keys()) + r')[-\s]?)+\b'
    text = re.sub(pattern, replace_number, text, flags=re.IGNORECASE)

    # Füge Leerzeichen zwischen Zahlen und Wörtern ein
    text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)

    return text

def digits_to_words(text, language=None):
    """
    Wandelt Ziffern in einem Text in Zahlwörter um.

    :param text: Der zu verarbeitende Text
    :param language: Die zu verwendende Sprache (optional, wird automatisch erkannt wenn nicht angegeben)
    :return: Der Text mit umgewandelten Ziffern
    """
    if language is None:
        language = detect_language(text)
    number_dict = GERMAN_NUMBER_DICT if language == 'de' else ENGLISH_NUMBER_DICT
    reverse_dict = {v: k for k, v in number_dict.items()}

    def replace_number(match):
        number = int(match.group(0))
        print(f"DEBUG: Verarbeite Zahl: {number}")  # Debugausgabe

        if number in reverse_dict:
            # DEUTSCH: Korrekte Behandlung von "ein" vs. "eins"
            if language == 'de' and number == 1:
                return 'ein' if not match.group(0).strip() == '1' else 'eins'
            return reverse_dict[number]

        words = []
        if language == 'de':
            if number >= 1000000000:
                milliarden = number // 1000000000
                words.append(f"{digits_to_words(str(milliarden), 'de')} Milliarden")
                number %= 1000000000
            if number >= 1000000:
                millionen = number // 1000000
                print(f"DEBUG: Millionen: {millionen}")  # Debugausgabe
                # DEUTSCH: Korrekte Behandlung von "Million" und "Millionen"
                if millionen == 1:
                    words.append("eine Million")
                else:
                    words.append(f"{digits_to_words(str(millionen), 'de')} Millionen")
                number %= 1000000
            if number >= 1000:
                tausende = number // 1000
                # DEUTSCH: Korrekte Behandlung von "eintausend"
                if tausende == 1:
                    words.append("eintausend")
                else:
                    words.append(f"{digits_to_words(str(tausende), 'de')}tausend")
                number %= 1000
            if number >= 100:
                hundreds = number // 100
                words.append(f"{reverse_dict[hundreds]}hundert")
                number %= 100
            if number > 0:
                if number <= 20:
                    words.append(reverse_dict[number])
                else:
                    ones = number % 10
                    tens = number - ones
                    # DEUTSCH: "ein" statt "eins" für Zahlen größer 20
                    if ones > 0:
                        if ones == 1:
                            words.append(f"einund{reverse_dict[tens]}")
                        else:
                            words.append(f"{reverse_dict[ones]}und{reverse_dict[tens]}")
                    else:
                        words.append(reverse_dict[tens])
        else:  # Englisch
            if number >= 1000000000:
                billions = number // 1000000000
                words.append(f"{digits_to_words(str(billions), 'en')} Billion")
                number %= 1000000000
            if number >= 1000000:
                millions = number // 1000000
                words.append(f"{digits_to_words(str(millions), 'en')} Million")
                number %= 1000000
            if number >= 1000:
                thousands = number // 1000
                words.append(f"{digits_to_words(str(thousands), 'en')} Thousand")
                number %= 1000
            if number >= 100:
                hundreds = number // 100
                words.append(f"{reverse_dict[hundreds]} Hundred")
                number %= 100
            if number > 0:
                if number <= 20:
                    words.append(reverse_dict[number])
                else:
                    tens = number // 10 * 10
                    ones = number % 10
                    if ones > 0:
                        words.append(f"{reverse_dict[tens]}-{reverse_dict[ones]}")
                    else:
                        words.append(reverse_dict[tens])

        result = "".join(words)
        print(f"DEBUG: Ergebnis vor Leerzeichenkorrektur: {result}")  # Debugausgabe
        # DEUTSCH: Leerzeichen nur zwischen Millionen und dem Rest beibehalten: Nur für Millionen und Milliarden, nicht für kleinere Zahlen
        if language == 'de':
            if "Million" in result:
                parts = result.split("Million")
                result = "Million ".join(parts)
            elif "Milliarden" in result:
                parts = result.split("Milliarden")
                result = "Milliarden ".join(parts)
        print(f"DEBUG: Finales Ergebnis: {result}")  # Debugausgabe
        return result.strip()

    return re.sub(r'\b\d+\b', replace_number, text)

def test_conversion(original):
    """
    Testet die Konvertierung von Zahlwörtern zu Ziffern und zurück.

    :param original: Der zu testende Originaltext
    """
    print(f"Original: {original}")
    to_digits = words_to_digits(original)
    print(f"Zahlwörter zu Ziffern: {to_digits}")
    to_words = digits_to_words(to_digits, detect_language(original))
    if to_words == original:
        print(colored(f"Ziffern zu Zahlwörtern: {to_words}", "green"))
    else:
        print(colored(f"Ziffern zu Zahlwörtern: {to_words}", "red"))
    print()

# Testfunktion
if __name__ == "__main__":
    test_texts = [
        "Ich habe dreiundzwanzig Äpfel und vierhundertsechsundfünfzig Birnen.",
        "I have twenty-three apples and four hundred fifty-six pears.",
        "eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn. Das ist ein kleiner Test.",
        "Das ist eine kleine Übung. 12, 21, 23, 45, 678, 1011, 4567",
        "Das ist ein kleiner Test. zwölf, dreiundzwanzig, fünfundvierzig, viertausendfünfhundertsiebenundsechzig",
        "zweitausend",
        "zwanzigtausend",
        "einundzwanzigtausend",
        "zweihunderttausend",
        "dreihundertfünfundvierzigtausend",
        "eine Million zweihunderttausenddreihundertfünfundvierzig",
        "zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig"
    ]

    for test_text in test_texts:
        test_conversion(test_text)

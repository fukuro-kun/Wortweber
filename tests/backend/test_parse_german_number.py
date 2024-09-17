import unittest

GERMAN_NUMBER_DICT = {
    'null': 0, 'ein': 1, 'eine': 1, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5,
    'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12,
    'dreizehn': 13, 'vierzehn': 14, 'fünfzehn': 15, 'sechzehn': 16, 'siebzehn': 17,
    'achtzehn': 18, 'neunzehn': 19, 'zwanzig': 20, 'dreißig': 30, 'vierzig': 40,
    'fünfzig': 50, 'sechzig': 60, 'siebzig': 70, 'achtzig': 80, 'neunzig': 90,
    'hundert': 100, 'tausend': 1000, 'million': 1000000, 'millionen': 1000000,
    'milliarde': 1000000000, 'milliarden': 1000000000
}

def parse_german_number(words):
    if isinstance(words, list) and len(words) == 1:
        words = words[0]

    print(f"DEBUG: Startworte: {words}")

    # Schritt 1: Ziffern und Operatoren extrahieren
    tokens = []
    remaining_word = words.lower()
    while remaining_word:
        if remaining_word.startswith('und'):
            tokens.append('+')
            remaining_word = remaining_word[3:]
        else:
            found = False
            for key, val in sorted(GERMAN_NUMBER_DICT.items(), key=lambda x: len(x[0]), reverse=True):
                if remaining_word.startswith(key):
                    tokens.append(val)
                    remaining_word = remaining_word[len(key):]
                    found = True
                    break
            if not found:
                remaining_word = remaining_word[1:]

    print(f"DEBUG: Extrahierte Tokens: {tokens}")

    # Schritt 2: Tokens gruppieren und Gleichung erstellen
    equation = []
    current_group = 0
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '+':
            if i + 2 < len(tokens) and tokens[i+2] >= 1000:
                # Behandlung von Fällen wie "zweiundvierzigtausend"
                current_group += tokens[i+1]
                equation.extend([str(current_group), '*', str(tokens[i+2]), '+'])
                current_group = 0
                i += 3
            else:
                if current_group:
                    equation.append(str(current_group))
                    current_group = 0
                equation.append('+')
                i += 1
        elif token >= 1000:
            if current_group:
                equation.extend([str(current_group), '*', str(token), '+'])
                current_group = 0
            else:
                equation.extend([str(token), '+'])
            i += 1
        elif token == 100:
            current_group *= token
            i += 1
        else:
            current_group += token
            i += 1

    if current_group:
        equation.append(str(current_group))

    # Entferne überschüssige Operatoren am Ende
    while equation and equation[-1] in ['+', '*']:
        equation.pop()

    equation_str = ' '.join(equation)
    print(f"DEBUG: Generierte Gleichung: {equation_str}")

    # Schritt 3: Gleichung auswerten
    result = eval(equation_str)
    print(f"DEBUG: Endergebnis: {result}")

    return result

# Testklasse
class TestParseGermanNumber(unittest.TestCase):
    def test_parse_german_number(self):
        test_cases = [
            (["dreiundvierzig"], 43),
            (["siebenhundertachtundzwanzig"], 728),
            (["eintausendneunhundertneunundneunzig"], 1999),
            (["zweihundertzehntausendvier"], 210004),
            (["zweiundvierzigtausendzehn"], 42010),
            (["eine Million zweihunderttausenddreihundertfünfundvierzig"], 1200345),
            (["zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig"], 2345678),
            (["eine Milliarde zweihundertmillionen dreihunderttausend"], 1200300000),
            # Neue Testfälle
           # (["nullkommazwei"], 0),  # Dezimalzahlen werden nicht unterstützt, sollte 0 zurückgeben, wird später implementiert
            (["eins"], 1),
            (["einundzwanzig"], 21),
            (["zweiundzwanzigtausenddreihundertvierundfünfzig"], 22354),
            (["neunundneunzigtausendneunhundertneunundneunzig"], 99999),
            (["eine Million"], 1000000),
            (["zweitausendeinundzwanzig"], 2021),
            (["dreitausendsiebenhunderteinundzwanzig"], 3721),
            (["neunzehnhundertvierundachtzig"], 1984),  # Historische Jahreszahl
            (["zweitausendachtzehn"], 2018),
            (["einhunderteins"], 101),
            (["tausendeins"], 1001),  # Wie im Märchen
            (["eine Milliarde eins"], 1000000001),
            (["zweihundertmillionen"], 200000000),
            (["neunhundertneunundneunzigtausendneunhundertneunundneunzig"], 999999),
            (["eine Million eine"], 1000001),
            (["zweiundzwanzig Millionen dreihundertvierundfünfzigtausendsechshundertachtundsiebzig"], 22354678),
            (["dreizehnmillionenzweihundertvierunddreißigtausendfünfhundertsiebenundsechzig"], 13234567),
            (["vierundvierzig Milliarden siebenhundertdreiundzwanzig Millionen neunhunderteinundfünfzigtausendsechshundertachtundsiebzig"], 44723951678),
        ]

        for words, expected in test_cases:
            with self.subTest(words=words, expected=expected):
                result = parse_german_number(words)
                self.assertEqual(result, expected)
                print(f"Test für {words} abgeschlossen. Erwartet: {expected}, Erhalten: {result}\n")

if __name__ == '__main__':
    unittest.main()

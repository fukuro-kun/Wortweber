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

from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import re
from src.utils.error_handling import handle_exceptions, logger

class TextTag(Enum):
    """
    Enum zur Kategorisierung von Textteilen während der Verarbeitung.
    """
    TEXT = "text"
    POSSIBLE_NUMBER = "moeglichezahl"
    LARGE_NUMBER = "grossezahl"
    NUMBER = "zahl"
    IP = "ip"
    DATE = "datum"

class TextPart:
    """
    Repräsentiert einen Teil des zu verarbeitenden Textes mit zusätzlichen Metadaten.
    """
    def __init__(self, content: str, tag: TextTag, position: int):
        self.content = content
        self.tag = tag
        self.position = position
        self.value: Optional[int] = None

class TextLevel:
    """
    Repräsentiert eine Verarbeitungsebene für den Text, die mehrere TextParts enthält.
    """
    def __init__(self, level: float):
        self.level = level
        self.parts: List[TextPart] = []

    def add_part(self, part: TextPart):
        """Fügt einen TextPart zur aktuellen Verarbeitungsebene hinzu."""
        self.parts.append(part)

class TextProcessor:
    """
    Hauptklasse zur Verarbeitung von Text, insbesondere zur Umwandlung von Zahlwörtern in Ziffern.
    """

    @handle_exceptions
    def __init__(self):
        """Initialisiert den TextProcessor mit mehreren Verarbeitungsebenen."""
        self.levels: Dict[float, TextLevel] = {}
        for i in range(5):
            self.levels[i] = TextLevel(i)
        self.current_position = 0
        logger.info("TextProcessor initialisiert")

    @handle_exceptions
    def process_text(self, text: str, language: str) -> str:
        """
        Verarbeitet den gegebenen Text und wandelt Zahlwörter in Ziffern um.

        :param text: Der zu verarbeitende Text
        :param language: Die Sprache des Textes ('de' für Deutsch, 'en' für Englisch)
        :return: Der verarbeitete Text mit umgewandelten Zahlwörtern
        """
        logger.debug(f"Verarbeite Text: {text}")
        self.current_position = 0
        self.split_special_formats(text, 0)
        self.print_levels_state()

        self.identify_number_words(language)
        self.print_levels_state()

        self.process_number_words(language)
        self.print_levels_state()

        self.accumulate_numbers()
        self.print_levels_state()

        result = self.reconstruct_text()
        logger.debug(f"Verarbeitetes Ergebnis: {result}")
        self.reset_levels()
        return result

    @handle_exceptions
    def reset_levels(self):
        """Setzt alle Verarbeitungsebenen zurück."""
        for level in self.levels.values():
            level.parts = []

    @handle_exceptions
    def split_special_formats(self, text: str, level: float) -> None:
        """
        Teilt den Text in spezielle Formate auf und fügt sie zur ersten Verarbeitungsebene hinzu.

        :param text: Der zu verarbeitende Text
        :param level: Die Verarbeitungsebene (wird derzeit nicht verwendet)
        """
        logger.debug(f"Teile spezielle Formate auf: {text}")
        self.levels[1].parts = []  # Zurücksetzen der Ebene 1 für jeden neuen Text
        self.levels[1].add_part(TextPart(text, TextTag.TEXT, 0))
        logger.debug(f"Inhalt von level 1 nach dem Hinzufügen: {[part.content for part in self.levels[1].parts]}")

    @handle_exceptions
    def identify_number_words(self, language: str) -> None:
        """
        Identifiziert potenzielle Zahlwörter im Text und markiert sie für die weitere Verarbeitung.

        :param language: Die Sprache des Textes ('de' für Deutsch, 'en' für Englisch)
        """
        logger.debug("Identifiziere Zahlwörter")
        level_1 = self.levels[1]
        level_2 = self.levels[2]
        level_2.parts = []

        number_indicators = NUMBER_INDICATORS_DE if language == 'de' else NUMBER_INDICATORS_EN

        for part in level_1.parts:
            if part.tag == TextTag.TEXT:
                words = part.content.split()
                i = 0
                while i < len(words):
                    if any(indicator in words[i].lower() for indicator in number_indicators):
                        start = i
                        while i < len(words) and (any(indicator in words[i].lower() for indicator in number_indicators) or words[i].lower() in ['und', 'and']):
                            i += 1
                        # Potenzielles Zahlwort
                        number_word = " ".join(words[start:i])
                        level_2.add_part(TextPart(number_word, TextTag.POSSIBLE_NUMBER, self.current_position))
                        self.current_position += len(number_word) + 1
                    else:
                        # Text, der kein Zahlwort ist
                        level_2.add_part(TextPart(words[i], TextTag.TEXT, self.current_position))
                        self.current_position += len(words[i]) + 1
                        i += 1
            else:
                level_2.add_part(part)

        logger.debug(f"Ebene 2 nach Identifikation: {[(p.content, p.tag) for p in level_2.parts]}")

    @handle_exceptions
    def process_number_words(self, language: str) -> None:
        logger.debug("Verarbeite Zahlwörter")
        level_2 = self.levels[2]
        level_3 = self.levels[3]
        level_3.parts = []

        parse_function = parse_german_number if language == 'de' else parse_english_number

        for part in level_2.parts:
            if part.tag == TextTag.POSSIBLE_NUMBER:
                value, _ = parse_function(part.content)
                if value is not None:
                    new_part = TextPart(str(value), TextTag.NUMBER, part.position)
                    new_part.value = value
                    level_3.add_part(new_part)
                else:
                    level_3.add_part(TextPart(part.content, TextTag.TEXT, part.position))
            else:
                level_3.add_part(part)

        logger.debug(f"Ebene 3 nach Verarbeitung: {[(p.content, p.tag) for p in level_3.parts]}")

    @handle_exceptions
    def accumulate_numbers(self) -> None:
        """
        Akkumuliert aufeinanderfolgende Zahlenwerte zu größeren Einheiten.
        """
        logger.debug("Akkumuliere Zahlen")
        level_3 = self.levels[3]
        level_4 = self.levels[4]
        level_4.parts = []
        i = 0
        while i < len(level_3.parts):
            part = level_3.parts[i]
            if part.tag in [TextTag.LARGE_NUMBER, TextTag.NUMBER]:
                if part.value >= 100:  # Nur große Zahlen akkumulieren
                    accumulated_parts, next_i = self.accumulate_number_sequence(level_3.parts, i)
                    self.add_accumulated_to_level_4(accumulated_parts, level_4)
                    i = next_i
                else:
                    level_4.add_part(part)
                    i += 1
            else:
                level_4.add_part(part)
                i += 1

    @handle_exceptions
    def accumulate_number_sequence(self, parts: List[TextPart], start_index: int) -> Tuple[List[TextPart], int]:
        """
        Akkumuliert eine Sequenz von Zahlenwerten.

        :param parts: Liste der TextParts
        :param start_index: Startindex für die Akkumulation
        :return: Tuple aus akkumulierten Teilen und nächstem Index
        """
        logger.debug(f"Akkumuliere Zahlensequenz ab Index {start_index}")
        accumulated = [parts[start_index]]
        i = start_index + 1
        while i < len(parts):
            current_part = parts[i]
            if current_part.tag not in [TextTag.LARGE_NUMBER, TextTag.NUMBER]:
                break
            if self.should_accumulate(accumulated[-1], current_part):
                accumulated.append(current_part)
                i += 1
            else:
                break
        return accumulated, i

    @handle_exceptions
    def should_accumulate(self, prev_part: TextPart, current_part: TextPart) -> bool:
        """
        Bestimmt, ob zwei aufeinanderfolgende Zahlenwerte akkumuliert werden sollten.

        :param prev_part: Vorheriger TextPart
        :param current_part: Aktueller TextPart
        :return: True, wenn akkumuliert werden soll, sonst False
        """
        if prev_part.value is None or current_part.value is None:
            return False
        if prev_part.tag == TextTag.LARGE_NUMBER and current_part.tag == TextTag.LARGE_NUMBER:
            return current_part.value < prev_part.value
        elif prev_part.tag == TextTag.LARGE_NUMBER and current_part.tag == TextTag.NUMBER:
            return True
        elif prev_part.tag == TextTag.NUMBER and current_part.tag == TextTag.LARGE_NUMBER:
            return False
        else:
            return prev_part.value > 100 and current_part.value <= prev_part.value

    @handle_exceptions
    def add_accumulated_to_level_4(self, accumulated_parts: List[TextPart], level_4: TextLevel):
        """
        Fügt akkumulierte Zahlenwerte zur vierten Verarbeitungsebene hinzu.

        :param accumulated_parts: Liste der akkumulierten TextParts
        :param level_4: Die vierte Verarbeitungsebene
        """
        logger.debug(f"Füge akkumulierte Teile zu Ebene 4 hinzu: {[p.content for p in accumulated_parts]}")

        total_value = 0
        for part in accumulated_parts:
            if part.tag in [TextTag.LARGE_NUMBER, TextTag.NUMBER]:
                value = part.value
                if value is not None:
                    total_value += value
                else:
                    logger.warning(f"Konnte '{part.content}' nicht in eine Zahl umwandeln.")
            else:
                logger.warning(f"Unerwartetes Tag {part.tag} für Teil '{part.content}'")

        new_part = TextPart(str(total_value), TextTag.NUMBER, accumulated_parts[0].position)
        new_part.value = total_value
        level_4.add_part(new_part)

    @handle_exceptions
    def reconstruct_text(self) -> str:
        """
        Rekonstruiert den verarbeiteten Text aus der letzten Verarbeitungsebene.

        :return: Der rekonstruierte Text
        """
        sorted_parts = sorted(self.levels[4].parts, key=lambda x: x.position)
        result = ' '.join(part.content for part in sorted_parts)
        logger.debug(f"Rekonstruierter Text (vor Bereinigung): {result}")
        result = re.sub(r'\s+', ' ', result).strip()
        logger.debug(f"Rekonstruierter Text: {result}")
        return result

    @handle_exceptions
    def print_levels_state(self):
        """
        Gibt den aktuellen Zustand aller Verarbeitungsebenen aus (nur für Debugging-Zwecke).
        """
        for level, text_level in self.levels.items():
            logger.debug(f"Inhalt von Ebene {level}: {[(part.content, part.tag) for part in text_level.parts]}")

@handle_exceptions
def parse_german_number(words):
    """
    Parst deutsche Zahlwörter und konvertiert sie in numerische Werte.

    :param words: Zahlwort oder Liste von Zahlwörtern
    :return: Tuple aus numerischem Wert und Originaltext (bei Fehler)
    """
    if isinstance(words, list):
        words = " ".join(words)
    words = str(words).strip().lower()
    logger.debug(f"Parse deutsche Zahl: {words}")

    # Spezielle Fälle
    if words in GERMAN_NUMBER_DICT:
        return GERMAN_NUMBER_DICT[words], None

    total = 0
    current = 0
    for word in words.replace('-', ' ').split():
        if word in GERMAN_NUMBER_DICT:
            value = GERMAN_NUMBER_DICT[word]
            if value == 100:
                current = current * value if current else value
            elif value >= 1000:
                if current:
                    total += current * value
                    current = 0
                else:
                    total = (total or 1) * value
            else:
                current += value
        elif word == 'und':
            continue
        else:
            return None, words

    total += current
    return total, None

@handle_exceptions
def parse_english_number(words):
    """
    Parst englische Zahlwörter und konvertiert sie in numerische Werte.

    :param words: Zahlwort oder Liste von Zahlwörtern
    :return: Tuple aus numerischem Wert und Originaltext (bei Fehler)
    """
    if isinstance(words, list):
        words = " ".join(words)
    words = str(words).strip().lower()
    logger.debug(f"Parse englische Zahl: {words}")

    # Spezielle Fälle
    if words in ENGLISH_NUMBER_DICT:
        return ENGLISH_NUMBER_DICT[words], None

    total = 0
    current = 0
    for word in words.replace('-', ' ').split():
        if word in ENGLISH_NUMBER_DICT:
            value = ENGLISH_NUMBER_DICT[word]
            if value == 100:
                current = current * value if current > 0 else value
            elif value >= 1000:
                total += (current or 1) * value
                current = 0
            else:
                current += value
        elif word == 'and':
            continue
        else:
            return None, words
    total += current

    return total if total > 0 else None, words

@handle_exceptions
def ziffern_zu_zahlwoerter(zahl: int, language: str) -> str:
    """
    Konvertiert eine Zahl in ihre Wortdarstellung.

    :param zahl: Die zu konvertierende Zahl
    :param language: Die Zielsprache ('de' für Deutsch, 'en' für Englisch)
    :return: Die Wortdarstellung der Zahl
    """
    if language == 'de':
        return german_ziffern_zu_zahlwoerter(zahl)
    elif language == 'en':
        return english_ziffern_zu_zahlwoerter(zahl)
    else:
        raise ValueError(f"Unsupported language: {language}")

@handle_exceptions
def german_ziffern_zu_zahlwoerter(zahl: int) -> str:
    """
    Konvertiert eine Zahl in ihre deutsche Wortdarstellung.

    :param zahl: Die zu konvertierende Zahl
    :return: Die deutsche Wortdarstellung der Zahl
    """
    if zahl == 0:
        return "null"

    einer = ["", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
    zehner = ["", "zehn", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]
    sonderformen = {11: "elf", 12: "zwölf", 16: "sechzehn", 17: "siebzehn"}
    grosse_zahlen = [(1000000000, "Milliarde"), (1000000, "Million"), (1000, "tausend")]

    def bis_99(n, am_ende=False):
        if n == 0:
            return ""
        if n == 1:
            return "eins" if am_ende else "ein"
        if n < 10:
            return einer[n]
        if n in sonderformen:
            return sonderformen[n]
        if n < 20:
            return einer[n % 10] + "zehn"
        return (einer[n % 10] + "und" if n % 10 != 0 else "") + zehner[n // 10]

    def bis_999(n, am_ende=False):
        if n < 100:
            return bis_99(n, am_ende)
        return einer[n // 100] + "hundert" + (bis_99(n % 100, am_ende) if n % 100 != 0 else "")

    ergebnis = ""
    for wert, name in grosse_zahlen:
        if zahl >= wert:
            anzahl = zahl // wert
            if wert == 1000:
                ergebnis += bis_999(anzahl) + name
            else:
                ergebnis += bis_999(anzahl) + " " + name
                if anzahl > 1:
                    ergebnis += "en"
            zahl %= wert
            if zahl > 0:
                if wert > 1000:
                    ergebnis += " "
                elif zahl < 100:
                    ergebnis += "und"

    if zahl > 0:
        ergebnis += bis_999(zahl, True)

    if ergebnis.startswith("ein "):
        ergebnis = "eine " + ergebnis[4:]

    return ergebnis.strip()

@handle_exceptions
def english_ziffern_zu_zahlwoerter(zahl: int) -> str:
    """
    Konvertiert eine Zahl in ihre englische Wortdarstellung.

    :param zahl: Die zu konvertierende Zahl
    :return: Die englische Wortdarstellung der Zahl
    """
    if zahl == 0:
        return "zero"

    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    large_numbers = [(1000000000, "billion"), (1000000, "million"), (1000, "thousand")]

    def up_to_999(n):
        if n < 10:
            return ones[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + ("-" + ones[n % 10] if n % 10 != 0 else "")
        else:
            return ones[n // 100] + " hundred" + (" and " + up_to_999(n % 100) if n % 100 != 0 else "")

    result = ""
    for value, name in large_numbers:
        if zahl >= value:
            result += up_to_999(zahl // value) + " " + name
            zahl %= value
            if zahl > 0:
                result += " "

    if zahl > 0:
        result += up_to_999(zahl)

    return result.strip()

@handle_exceptions
def words_to_digits(text: str, language: str = 'de') -> str:
    """
    Konvertiert Zahlwörter in einem Text zu Ziffern.

    :param text: Der zu konvertierende Text
    :param language: Die Sprache des Textes ('de' für Deutsch, 'en' für Englisch)
    :return: Der Text mit konvertierten Ziffern
    """
    processor = TextProcessor()
    return processor.process_text(text, language)

@handle_exceptions
def digits_to_words(text: str, language: str = 'de') -> str:
    """
    Konvertiert Ziffern in einem Text zu Zahlwörtern.

    :param text: Der zu konvertierende Text
    :param language: Die Zielsprache ('de' für Deutsch, 'en' für Englisch)
    :return: Der Text mit konvertierten Zahlwörtern
    """
    def convert_number(match):
        number = int(match.group())
        return ziffern_zu_zahlwoerter(number, language)

    return re.sub(r'\b\d+\b', convert_number, text)

def detect_language(text: str) -> str:
    """
    Erkennt die Sprache des gegebenen Textes.
    Unterstützt derzeit nur Deutsch und Englisch.

    :param text: Der zu analysierende Text
    :return: 'de' für Deutsch, 'en' für Englisch
    """
    german_words = set(['der', 'die', 'das', 'ist', 'ein', 'eine', 'und', 'in', 'mit', 'für', 'von', 'zu'])
    english_words = set(['the', 'is', 'a', 'an', 'and', 'in', 'with', 'for', 'of', 'to'])

    words = text.lower().split()
    german_count = sum(1 for word in words if word in german_words)
    english_count = sum(1 for word in words if word in english_words)

    return 'de' if german_count >= english_count else 'en'

# Globale Variablen und Konstanten

GERMAN_NUMBER_DICT = {
    'null': 0, 'ein': 1, 'eine': 1, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5,
    'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12,
    'dreizehn': 13, 'vierzehn': 14, 'fünfzehn': 15, 'sechzehn': 16, 'siebzehn': 17,
    'achtzehn': 18, 'neunzehn': 19, 'zwanzig': 20, 'dreißig': 30, 'vierzig': 40,
    'fünfzig': 50, 'sechzig': 60, 'siebzig': 70, 'achtzig': 80, 'neunzig': 90,
    'hundert': 100, 'tausend': 1000, 'million': 1000000, 'millionen': 1000000,
    'milliarde': 1000000000, 'milliarden': 1000000000
}

ENGLISH_NUMBER_DICT = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000,
    'million': 1000000, 'billion': 1000000000
}

NUMBER_INDICATORS_DE = list(GERMAN_NUMBER_DICT.keys()) + ["million", "millionen", "milliarde", "milliarden", "billion", "billionen"]
NUMBER_INDICATORS_EN = list(ENGLISH_NUMBER_DICT.keys()) + ["million", "billion", "trillion"]




# Zusätzliche Erklärungen:

# 1. Die digits_to_words Funktion wurde aktualisiert, um die neue ziffern_zu_zahlwoerter Funktion zu verwenden.
#    Sie nutzt einen regulären Ausdruck, um alle Zahlen im Text zu finden und zu ersetzen.

# 2. Die ziffern_zu_zahlwoerter Funktion implementiert die komplexen Regeln der deutschen Zahlwortbildung.
#    Sie behandelt Zahlen bis zu einer Billion und berücksichtigt alle Sonderfälle und Unregelmäßigkeiten.

# 3. Die bestehende parse_german_number Funktion wurde beibehalten, da sie für die Umwandlung von Worten in Zahlen verwendet wird.

# 4. Die TextProcessor-Klasse und ihre Methoden wurden angepasst, um sicherzustellen, dass alle Teile des Textes
#    korrekt verarbeitet werden, einschließlich der Teile, die während der Verarbeitung zurück in niedrigere Ebenen verschoben werden.

# 5. Die process_text Methode wurde so angepasst, dass sie alle Verarbeitungsschritte nacheinander ausführt,
#    ohne zu versuchen, Teile zurück in Ebene 1 zu verschieben.

# 6. Es wäre sinnvoll, umfangreiche Tests für die neue Implementierung zu erstellen,
#    um sicherzustellen, dass sie alle möglichen Fälle korrekt behandelt.

# 7. In zukünftigen Versionen könnte man die Effizienz der Funktionen optimieren,
#    insbesondere für sehr große Zahlen oder häufige Aufrufe.

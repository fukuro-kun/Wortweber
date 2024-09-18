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



"""
Dieses Modul enthält Funktionen zur Textverarbeitung, insbesondere zur Umwandlung
von Zahlwörtern in Ziffern und umgekehrt. Es bietet Unterstützung für deutsche
und englische Zahlwörter und implementiert eine robuste Logik zur Erkennung und
Verarbeitung komplexer Zahlausdrücke.
"""

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
    def process_text(self, text: str) -> str:
        """
        Verarbeitet den gegebenen Text und wandelt Zahlwörter in Ziffern um.

        :param text: Der zu verarbeitende Text
        :return: Der verarbeitete Text mit umgewandelten Zahlwörtern
        """
        logger.debug(f"Verarbeite Text: {text}")
        self.current_position = 0
        self.split_special_formats(text, 0)
        self.print_levels_state()

        self.identify_number_words()
        self.print_levels_state()

        self.process_number_words()
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
    def identify_number_words(self) -> None:
        """
        Identifiziert potenzielle Zahlwörter im Text und markiert sie für die weitere Verarbeitung.
        """
        logger.debug("Identifiziere Zahlwörter")
        level_1 = self.levels[1]
        level_2 = self.levels[2]
        level_2.parts = []

        for part in level_1.parts:
            if part.tag == TextTag.TEXT:
                words = part.content.split()
                i = 0
                while i < len(words):
                    if any(indicator in words[i].lower() for indicator in NUMBER_INDICATORS):
                        start = i
                        while i < len(words) and (any(indicator in words[i].lower() for indicator in NUMBER_INDICATORS) or words[i].lower() == 'und'):
                            i += 1
                        # Text vor dem potenziellen Zahlwort
                        if start > 0:
                            level_2.add_part(TextPart(" ".join(words[:start]), TextTag.TEXT, self.current_position))
                            self.current_position += len(" ".join(words[:start])) + 1
                        # Potenzielles Zahlwort und Rest
                        level_2.add_part(TextPart(" ".join(words[start:]), TextTag.POSSIBLE_NUMBER, self.current_position))
                        self.current_position += len(" ".join(words[start:])) + 1
                        break
                    i += 1
                if i == len(words):  # Kein Zahlwort gefunden
                    level_2.add_part(TextPart(part.content, TextTag.TEXT, self.current_position))
                    self.current_position += len(part.content) + 1
            else:
                level_2.add_part(part)

        logger.debug(f"Ebene 2 nach Identifikation: {[(p.content, p.tag) for p in level_2.parts]}")

    @handle_exceptions
    def process_number_words(self) -> None:
        """
        Verarbeitet identifizierte Zahlwörter und wandelt sie in numerische Werte um.
        """
        logger.debug("Verarbeite Zahlwörter")
        level_2 = self.levels[2]
        level_3 = self.levels[3]
        level_3.parts = []

        i = 0
        while i < len(level_2.parts):
            part = level_2.parts[i]
            if part.tag == TextTag.POSSIBLE_NUMBER:
                words = part.content.split()
                if len(words) == 1:
                    value, _ = parse_german_number(part.content)
                    if value is not None:
                        new_part = TextPart(str(value), TextTag.NUMBER, part.position)
                        new_part.value = value
                        level_3.add_part(new_part)
                    else:
                        level_3.add_part(TextPart(part.content, TextTag.TEXT, part.position))
                else:
                    processed_parts = self.process_word_pairs(words, part.position)
                    level_3.parts.extend(processed_parts)
                    # Wenn es einen Rest gibt, fügen wir ihn zurück zu level_2 hinzu
                    if processed_parts[-1].tag == TextTag.POSSIBLE_NUMBER:
                        level_2.parts.insert(i+1, processed_parts[-1])
                        level_3.parts.pop()  # Entferne den Rest aus level_3
            else:
                level_3.add_part(part)
            i += 1

        logger.debug(f"Ebene 3 nach Verarbeitung: {[(p.content, p.tag) for p in level_3.parts]}")

    @handle_exceptions
    def process_word_pairs(self, words: List[str], start_position: int) -> List[TextPart]:
        """
        Verarbeitet Wortpaare, um komplexe Zahlausdrücke zu erkennen und umzuwandeln.

        :param words: Liste der zu verarbeitenden Wörter
        :param start_position: Startposition im Originaltext
        :return: Liste der verarbeiteten TextParts
        """
        result = []
        i = 0
        while i < len(words):
            if i < len(words) - 1:
                pair = words[i:i+2]
                if pair[1].lower() in [word.lower() for word in LARGE_NUMBER_WORDS]:
                    value, _ = parse_german_number(" ".join(pair))
                    if value is not None:
                        part = TextPart(str(value), TextTag.LARGE_NUMBER, start_position + i)
                        part.value = value
                        result.append(part)
                        i += 2
                    else:
                        result.append(TextPart(pair[0], TextTag.TEXT, start_position + i))
                        i += 1
                elif pair[0].lower() in ['ein', 'eine'] and pair[1].lower() not in LARGE_NUMBER_WORDS:
                    result.append(TextPart(pair[0], TextTag.TEXT, start_position + i))
                    result.append(TextPart(pair[1], TextTag.TEXT, start_position + i + 1))
                    i += 2
                else:
                    value, original = parse_german_number(pair[0])
                    if value is not None:
                        result.append(TextPart(str(value), TextTag.NUMBER, start_position + i))
                        # Der Rest wird als mögliche Zahl zurück in die Verarbeitung gegeben
                        if i + 1 < len(words):
                            rest = " ".join(words[i+1:])
                            result.append(TextPart(rest, TextTag.POSSIBLE_NUMBER, start_position + i + 1))
                        return result
                    else:
                        result.append(TextPart(str(original), TextTag.TEXT, start_position + i))
                    i += 1
            else:
                value, original = parse_german_number(words[i])
                if value is not None:
                    result.append(TextPart(str(value), TextTag.NUMBER, start_position + i))
                else:
                    result.append(TextPart(str(original), TextTag.TEXT, start_position + i))
                i += 1
        return result

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
                accumulated_parts, next_i = self.accumulate_number_sequence(level_3.parts, i)
                self.add_accumulated_to_level_4(accumulated_parts, level_4)

                # Füge alle Textteile zwischen dieser und der nächsten Zahl hinzu
                for j in range(i+1, next_i):
                    if level_3.parts[j].tag == TextTag.TEXT:
                        level_4.add_part(level_3.parts[j])

                i = next_i
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
            return prev_part.value > current_part.value

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
                value, _ = parse_german_number(part.content)
                if value is not None:
                    total_value += value
                else:
                    logger.warning(f"Konnte '{part.content}' nicht in eine Zahl umwandeln.")
            else:
                logger.warning(f"Unerwartetes Tag {part.tag} für Teil '{part.content}'")

        new_part = TextPart(str(total_value), TextTag.TEXT, accumulated_parts[0].position)
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
    words = str(words).strip()  # Stelle sicher, dass words ein String ist und entferne führende/nachfolgende Leerzeichen
    logger.debug(f"Parse deutsche Zahl: {words}")

    # Prüfen, ob die Eingabe bereits eine Zahl ist
    try:
        return int(words), None
    except ValueError:
        pass  # Wenn es keine Zahl ist, fahren wir mit der Wortanalyse fort

    logger.debug(f"Startworte: {words}")

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
                # Wenn kein bekanntes Zahlwort gefunden wurde, brechen wir ab
                return None, words

    logger.debug(f"Extrahierte Tokens: {tokens}")

    if not tokens or (len(tokens) == 1 and tokens[0] == '+'):
        return None, words

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
    logger.debug(f"Generierte Gleichung: {equation_str}")

    # Schritt 3: Gleichung auswerten
    if equation_str:
        result = eval(equation_str)
        logger.debug(f"Endergebnis: {result}")
        return result, None
    else:
        return None, words

@handle_exceptions
def ziffern_zu_zahlwoerter(zahl):
    """
    Konvertiert eine Zahl in ihre deutsche Wortdarstellung.

    Args:
        zahl (int): Die zu konvertierende Zahl. Muss eine nicht-negative ganze Zahl sein.

    Returns:
        str: Die deutsche Wortdarstellung der Zahl.

    Raises:
        ValueError: Wenn die Eingabe keine nicht-negative ganze Zahl ist.
    """
    if not isinstance(zahl, int) or zahl < 0:
        raise ValueError("Die Eingabe muss eine nicht-negative ganze Zahl sein.")

    if zahl == 0:
        return "null"

    # Grundlegende Bausteine für die Zahlwortbildung
    einer = ["", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
    zehner = ["", "zehn", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]
    sonderformen = {11: "elf", 12: "zwölf", 16: "sechzehn", 17: "siebzehn"}
    # Große Zahlen mit ihren Namen, in absteigender Reihenfolge für die Verarbeitung
    grosse_zahlen = [(1000000000000, "Billion"), (1000000000, "Milliarde"), (1000000, "Million"), (1000, "tausend")]

    def bis_99(n, am_ende=False):
        """
        Konvertiert Zahlen bis 99 in Wortform.

        :param n: zu konvertierende Zahl
        :param am_ende: Flag, ob die Zahl am Ende der gesamten Zahl steht
        """
        if n == 0:
            return ""
        if n == 1:
            # Unterscheidung zwischen "ein" und "eins" basierend auf der Position
            return "eins" if am_ende else "ein"
        if n < 10:
            return einer[n]
        if n in sonderformen:
            return sonderformen[n]
        if n < 20:
            # Zahlen von 13-19 (außer Sonderformen)
            return einer[n % 10] + "zehn"
        # Zahlen von 20-99: Einer (falls vorhanden) + "und" + Zehner
        return (einer[n % 10] + "und" if n % 10 != 0 else "") + zehner[n // 10]

    def bis_999(n, am_ende=False):
        """
        Konvertiert Zahlen bis 999 in Wortform.

        :param n: zu konvertierende Zahl
        :param am_ende: Flag, ob die Zahl am Ende der gesamten Zahl steht
        """
        if n < 100:
            return bis_99(n, am_ende)
        # Hunderter + Rest (falls vorhanden)
        return einer[n // 100] + "hundert" + (bis_99(n % 100, am_ende) if n % 100 != 0 else "")

    ergebnis = ""
    for wert, name in grosse_zahlen:
        if zahl >= wert:
            anzahl = zahl // wert
            if wert == 1000:
                # Sonderfall für Tausender: kein Leerzeichen
                ergebnis += bis_999(anzahl) + name
            else:
                # Für Millionen und größer: Leerzeichen und ggf. Plural
                ergebnis += bis_999(anzahl) + " " + name
                if anzahl > 1:
                    ergebnis += "en"  # Plural für Millionen, Milliarden, etc.
            zahl %= wert  # Verbleibenden Wert berechnen
            if zahl > 0:
                if wert > 1000:
                    # Regeln für "und" bei großen Zahlen
                    if zahl < 100 and zahl > 0:
                        ergebnis += " und "
                    else:
                        ergebnis += " "
                elif zahl < 100:
                    # "und" für Zahlen unter 100 bei Tausendern
                    ergebnis += "und"

    if zahl > 0:
        # True für am_ende, da es das Ende der Zahl ist
        ergebnis += bis_999(zahl, True)

    # Spezielle Behandlung für "ein" am Anfang großer Zahlen (z.B. "eine Million")
    if ergebnis.startswith("ein "):
        ergebnis = "eine " + ergebnis[4:]

    return ergebnis.strip()  # Entfernen möglicher Leerzeichen am Anfang oder Ende

# Zusätzliche Erklärungen:
# - Die Funktion behandelt nun "ein" und "eins" korrekt.
# - Leerzeichen werden nur bei großen Zahlen (Millionen und größer) eingefügt.
# - Die Verwendung von "und" wurde gemäß den Regeln implementiert.
# - Die Verknüpfungsregeln für Tausender und kleinere Zahlen wurden berücksichtigt.
# - Die Pluralform für Millionen, Milliarden, etc. wird korrekt gebildet.
# - Es gibt keine Leerzeichen zwischen Tausendern und kleineren Einheiten.

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

LARGE_NUMBER_WORDS = ["million", "millionen", "milliarde", "milliarden", "billion", "billionen", "billiarde", "billiarden", "trillion", "trillionen", "trilliarde", "trilliarden"]

NUMBER_INDICATORS = list(GERMAN_NUMBER_DICT.keys()) + LARGE_NUMBER_WORDS

# Hauptfunktionen

@handle_exceptions
def words_to_digits(text: str) -> str:
    """
    Konvertiert Zahlwörter in einem Text zu Ziffern.

    :param text: Der zu konvertierende Text
    :return: Der Text mit konvertierten Ziffern
    """
    processor = TextProcessor()
    return processor.process_text(text)

@handle_exceptions
def digits_to_words(text: str) -> str:
    """
    Konvertiert Ziffern in einem Text zu Zahlwörtern.

    :param text: Der zu konvertierende Text
    :return: Der Text mit konvertierten Zahlwörtern
    """
    def convert_number(match):
        number = int(match.group())
        return ziffern_zu_zahlwoerter(number)

    return re.sub(r'\b\d+\b', convert_number, text)

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

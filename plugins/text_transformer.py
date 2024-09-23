from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions, logger
from typing import Dict, Any

class TextTransformerPlugin(AbstractPlugin):
    def __init__(self):
        self.settings = self.get_default_settings()

    @property
    def name(self) -> str:
        return "TextTransformer"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Transformiert Text in Großbuchstaben und fügt optional ein Präfix hinzu."

    @property
    def author(self) -> str:
        return "Wortweber Team"

    @handle_exceptions
    def get_default_settings(self) -> Dict[str, Any]:
        return {
            "prefix": "",
            "max_chars": 1000
        }

    @handle_exceptions
    def activate(self, settings: Dict[str, Any]) -> None:
        self.settings.update(settings)
        logger.info(f"TextTransformer Plugin aktiviert mit Einstellungen: {self.settings}")

    @handle_exceptions
    def deactivate(self) -> Dict[str, Any]:
        logger.info("TextTransformer Plugin deaktiviert")
        return self.settings

    @handle_exceptions
    def process_text(self, text: str) -> str:
        max_chars = int(self.settings.get("max_chars", 1000))
        prefix = self.settings.get("prefix", "")

        limited_text = text[:max_chars]
        transformed_text = prefix + limited_text.upper()

        logger.info(f"Text transformiert: {len(text)} Zeichen eingegeben, {len(transformed_text)} Zeichen ausgegeben")
        return transformed_text

    @handle_exceptions
    def get_settings(self) -> Dict[str, Any]:
        return self.settings

    @handle_exceptions
    def set_settings(self, settings: Dict[str, Any]) -> None:
        self.settings.update(settings)
        logger.info(f"Neue Einstellungen für TextTransformer gesetzt: {self.settings}")

    @handle_exceptions
    def update_settings(self, settings: Dict[str, Any]) -> None:
        self.set_settings(settings)
        logger.info(f"Einstellungen für TextTransformer aktualisiert: {self.settings}")
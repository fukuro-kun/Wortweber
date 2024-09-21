from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions, logger

class TextTransformerPlugin(AbstractPlugin):
    def __init__(self):
        self.settings = self.get_default_settings()

    @property
    def name(self):
        return "TextTransformer"

    @property
    def version(self):
        return "1.0.0"

    @property
    def description(self):
        return "Transformiert Text in Großbuchstaben und fügt optional ein Präfix hinzu."

    @property
    def author(self):
        return "Wortweber Team"

    @handle_exceptions
    def get_default_settings(self):
        return {
            "prefix": "",
            "max_chars": 1000
        }

    @handle_exceptions
    def activate(self, settings):
        self.settings.update(settings)
        logger.info(f"TextTransformer Plugin aktiviert mit Einstellungen: {self.settings}")

    @handle_exceptions
    def deactivate(self):
        logger.info("TextTransformer Plugin deaktiviert")
        return self.settings

    @handle_exceptions
    def process_text(self, text):
        max_chars = int(self.settings.get("max_chars", 1000))
        prefix = self.settings.get("prefix", "")

        limited_text = text[:max_chars]
        transformed_text = prefix + limited_text.upper()

        logger.info(f"Text transformiert: {len(text)} Zeichen eingegeben, {len(transformed_text)} Zeichen ausgegeben")
        return transformed_text

    @handle_exceptions
    def get_settings(self):
        return self.settings

    @handle_exceptions
    def set_settings(self, settings):
        self.settings.update(settings)
        logger.info(f"Neue Einstellungen für TextTransformer gesetzt: {self.settings}")

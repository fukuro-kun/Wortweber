from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions
from typing import Dict, Any

class UppercasePlugin(AbstractPlugin):
    def __init__(self):
        self.settings = self.get_default_settings()

    @property
    def name(self) -> str:
        return "UppercaseConverter"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Konvertiert Text in Großbuchstaben"

    @property
    def author(self) -> str:
        return "Wortweber Team"

    @handle_exceptions
    def get_default_settings(self) -> Dict[str, Any]:
        return {}

    @handle_exceptions
    def activate(self, settings: Dict[str, Any]) -> None:
        self.settings.update(settings)

    @handle_exceptions
    def deactivate(self) -> Dict[str, Any]:
        return self.settings

    @handle_exceptions
    def process_text(self, text: str) -> str:
        return text.upper()

    @handle_exceptions
    def get_settings(self) -> Dict[str, Any]:
        return self.settings

    @handle_exceptions
    def set_settings(self, settings: Dict[str, Any]) -> None:
        self.settings.update(settings)

    @handle_exceptions
    def update_settings(self, settings: Dict[str, Any]) -> None:
        self.set_settings(settings)

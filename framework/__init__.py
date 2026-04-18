"""GenAI Locator Healing Framework"""

from .locator_registry import LocatorRegistry, LocatorConfig
from .genai_healer import GenAILocatorHealer
from .smart_finder import SmartElementFinder

__version__ = "1.0.0"
__all__ = [
    "LocatorRegistry",
    "LocatorConfig",
    "GenAILocatorHealer",
    "SmartElementFinder",
]
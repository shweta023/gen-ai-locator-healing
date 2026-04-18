"""Smart Element Finder with auto-healing capabilities - ENHANCED WITH DEBUG LOGGING"""

import time
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)
from .locator_registry import LocatorRegistry
from .genai_healer import GenAILocatorHealer


class SmartElementFinder:
    """Enhanced element finder with auto-healing capabilities and detailed logging"""

    def __init__(
            self,
            driver: webdriver.Chrome,
            registry: LocatorRegistry,
            healer: GenAILocatorHealer,
            auto_heal: bool = True,
            max_heal_attempts: int = 3,
            verbose: bool = True  # Add verbose logging option
    ):
        self.driver = driver
        self.registry = registry
        self.healer = healer
        self.auto_heal = auto_heal
        self.max_heal_attempts = max_heal_attempts
        self.verbose = verbose
        self.healing_log: List[Dict] = []

    def find_element(self, locator_name: str, timeout: int = 10):
        """
        Find element with auto-healing on failure - ENHANCED LOGGING

        Args:
            locator_name: Name of the locator in registry
            timeout: Wait timeout in seconds

        Returns:
            WebElement if found

        Raises:
            ValueError: If locator not in registry
            TimeoutException: If element not found and healing failed
        """
        locator_config = self.registry.get_locator(locator_name)
        if not locator_config:
            raise ValueError(f"Locator '{locator_name}' not found in registry")

        # Convert string to By constant
        by_strategy = self._get_by_strategy(locator_config.by)

        try:
            # Try to find element normally
            if self.verbose:
                print(f"🔍 Looking for element: {locator_name}")
                print(f"   Strategy: {locator_config.by} = '{locator_config.value}'")
                print(f"   Description: {locator_config.description}")

            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_strategy, locator_config.value))
            )

            if self.verbose:
                print(f"✅ Found element: {locator_name}")

            return element

        except (TimeoutException, NoSuchElementException) as e:
            if self.verbose:
                print(f"\n❌ Failed to find element: {locator_name}")
                print(f"   Current URL: {self.driver.current_url}")
                print(f"   Page title: {self.driver.title}")
                print(f"   Strategy used: {locator_config.by}")
                print(f"   Value used: '{locator_config.value}'")

            self.registry.increment_failure(locator_name)

            # Get updated failure count
            updated_config = self.registry.get_locator(locator_name)

            if self.verbose:
                print(f"   Failure count: {updated_config.failure_count}")
                print(f"   Max attempts: {self.max_heal_attempts}")
                print(f"   Auto-heal enabled: {self.auto_heal}")

            # Check if we should attempt healing
            if self.auto_heal and updated_config.failure_count <= self.max_heal_attempts:
                if self.verbose:
                    print(f"\n🔧 ===== STARTING AUTO-HEAL =====")
                    print(f"   Locator: {locator_name}")
                    print(f"   Attempt: {updated_config.failure_count}/{self.max_heal_attempts}")
                    print(f"   GenAI client available: {self.healer.client is not None}")

                healed = self._attempt_healing(updated_config)

                if healed:
                    if self.verbose:
                        print(f"✅ Healing successful! Retrying...")
                    time.sleep(1)  # Brief pause before retry
                    return self.find_element(locator_name, timeout)
                else:
                    if self.verbose:
                        print(f"❌ Healing failed for: {locator_name}")
            else:
                if not self.auto_heal:
                    if self.verbose:
                        print(f"⚠️  Auto-heal is DISABLED")
                else:
                    if self.verbose:
                        print(f"⛔ Max healing attempts ({self.max_heal_attempts}) exceeded")
                        print(f"   Total failures: {updated_config.failure_count}")

            # Re-raise original exception
            raise e

    def find_elements(self, locator_name: str, timeout: int = 10):
        """Find multiple elements (returns list)"""
        locator_config = self.registry.get_locator(locator_name)
        if not locator_config:
            raise ValueError(f"Locator '{locator_name}' not found in registry")

        by_strategy = self._get_by_strategy(locator_config.by)

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_strategy, locator_config.value))
            )
            elements = self.driver.find_elements(by_strategy, locator_config.value)

            if self.verbose:
                print(f"✅ Found {len(elements)} elements: {locator_name}")

            return elements
        except Exception as e:
            if self.verbose:
                print(f"❌ Failed to find elements: {locator_name}")
            raise e

    def _attempt_healing(self, locator) -> bool:
        """Attempt to heal a broken locator - ENHANCED LOGGING"""
        if self.verbose:
            print(f"\n🏥 ===== HEALING PROCESS =====")
            print(f"   Locator name: {locator.name}")
            print(f"   Page: {locator.page}")
            print(f"   Current strategy: {locator.by}")
            print(f"   Current value: '{locator.value}'")
            print(f"   Description: {locator.description}")

        # Check if GenAI is available
        if not self.healer.client:
            if self.verbose:
                print(f"   ❌ GenAI client not available!")
                print(f"   API key present: {self.healer.api_key is not None}")
            return False

        # Use GenAI to suggest new locator
        if self.verbose:
            print(f"\n   📡 Calling GenAI API...")
            print(f"   Model: claude-sonnet-4-20250514")

        try:
            suggestion = self.healer.analyze_page_and_suggest_locator(
                self.driver,
                locator,
                self.driver.page_source
            )
        except Exception as e:
            if self.verbose:
                print(f"   ❌ GenAI API call failed: {str(e)}")
            return False

        if not suggestion:
            if self.verbose:
                print(f"   ❌ GenAI returned NO suggestion")
            return False

        if self.verbose:
            print(f"\n   ✅ GenAI Suggestion Received:")
            print(f"      Strategy: {suggestion['by']}")
            print(f"      Value: '{suggestion['value']}'")
            print(f"      Confidence: {suggestion['confidence']}")
            print(f"      Reasoning: {suggestion['reasoning']}")

        # Verify the suggestion works
        try:
            by_strategy = self._get_by_strategy(suggestion['by'])

            if self.verbose:
                print(f"\n   🧪 Testing suggested locator...")
                print(f"      Looking for: {suggestion['by']} = '{suggestion['value']}'")

            test_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by_strategy, suggestion['value']))
            )

            if test_element:
                if self.verbose:
                    print(f"   ✅ Suggested locator WORKS!")
                    print(f"\n   💾 Updating registry...")

                # Update registry
                old_value = locator.value
                old_by = locator.by

                self.registry.update_locator(
                    locator.name,
                    suggestion['value'],
                    suggestion['by']
                )

                if self.verbose:
                    print(f"   ✅ Registry updated:")
                    print(f"      {old_by}='{old_value}' → {suggestion['by']}='{suggestion['value']}'")

                # Log the healing
                healing_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'locator_name': locator.name,
                    'page': locator.page,
                    'old_by': old_by,
                    'old_value': old_value,
                    'new_by': suggestion['by'],
                    'new_value': suggestion['value'],
                    'confidence': suggestion['confidence'],
                    'reasoning': suggestion['reasoning']
                }
                self.healing_log.append(healing_entry)

                if self.verbose:
                    print(f"   ✅ Healing logged to report")
                    print(f"🏥 ===== HEALING SUCCESSFUL =====\n")

                return True

        except Exception as e:
            if self.verbose:
                print(f"   ❌ Suggested locator verification FAILED:")
                print(f"      Error: {str(e)}")
                print(f"      The suggested locator doesn't work on the page")
                print(f"🏥 ===== HEALING FAILED =====\n")
            return False

        return False

    def _get_by_strategy(self, by_string: str):
        """Convert string to By constant"""
        by_map = {
            'ID': By.ID,
            'NAME': By.NAME,
            'XPATH': By.XPATH,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'CLASS_NAME': By.CLASS_NAME,
            'TAG_NAME': By.TAG_NAME,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
        }
        return by_map.get(by_string.upper(), By.XPATH)

    def get_healing_report(self) -> List[Dict]:
        """Get report of all healing attempts"""
        return self.healing_log

    def print_healing_report(self):
        """Print formatted healing report"""
        if not self.healing_log:
            print("\n✅ No locators needed healing during this session!")
            return

        print("\n" + "=" * 70)
        print("🏥 LOCATOR HEALING REPORT")
        print("=" * 70)

        for i, entry in enumerate(self.healing_log, 1):
            print(f"\n[{i}] Locator: {entry['locator_name']} (Page: {entry['page']})")
            print(f"    Old: {entry['old_by']} = {entry['old_value']}")
            print(f"    New: {entry['new_by']} = {entry['new_value']}")
            print(f"    Confidence: {entry['confidence']}")
            print(f"    Reasoning: {entry['reasoning']}")
            print(f"    Time: {entry['timestamp']}")

        print("\n" + "=" * 70)
        print(f"Total Healings: {len(self.healing_log)}")
        print("=" * 70 + "\n")
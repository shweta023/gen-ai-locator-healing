"""
Mock GenAI Healer - Test the framework without an API key
This simulates the GenAI behavior with predefined rules
"""

from typing import Dict, Optional
from selenium import webdriver
from framework.locator_registry import LocatorConfig


class MockGenAILocatorHealer:
    """
    Mock GenAI healer that uses predefined rules instead of API calls
    Perfect for testing without API key
    """

    def __init__(self, api_key: str = None):
        self.api_key = "mock-key"
        self.client = True  # Mock client (not None)
        print("✅ Mock GenAI Healer initialized (no API key needed)")

    def analyze_page_and_suggest_locator(
            self,
            driver: webdriver.Chrome,
            broken_locator: LocatorConfig,
            page_source: str = None
    ) -> Optional[Dict[str, str]]:
        """
        Mock GenAI analysis using predefined rules

        This simulates what the real GenAI would suggest
        """
        print(f"🤖 Mock GenAI: Analyzing locator '{broken_locator.name}'")
        print(f"   Current value: '{broken_locator.value}'")

        # Get page source if not provided
        if not page_source:
            page_source = driver.page_source

        # Apply mock logic based on locator name and description
        suggestion = self._get_mock_suggestion(broken_locator, page_source, driver)

        if suggestion:
            print(f"   ✅ Mock suggestion: {suggestion['by']} = '{suggestion['value']}'")
        else:
            print(f"   ❌ No mock suggestion available")

        return suggestion

    def _get_mock_suggestion(
            self,
            locator: LocatorConfig,
            page_source: str,
            driver: webdriver.Chrome
    ) -> Optional[Dict[str, str]]:
        """
        Generate mock suggestions based on common patterns
        """

        # Strategy 1: Try to find element by examining page source
        # Look for common patterns in the description
        description_lower = locator.description.lower()

        # For login page elements
        if 'username' in description_lower or 'user' in description_lower:
            if self._element_exists(driver, 'id', 'username'):
                return {
                    'by': 'ID',
                    'value': 'username',
                    'confidence': 'high',
                    'reasoning': 'Found input field with id="username" which matches description for username input'
                }

        if 'password' in description_lower:
            if self._element_exists(driver, 'id', 'password'):
                return {
                    'by': 'ID',
                    'value': 'password',
                    'confidence': 'high',
                    'reasoning': 'Found input field with id="password" which matches description for password input'
                }

        if 'submit' in description_lower or 'login' in description_lower:
            if self._element_exists(driver, 'css selector', 'button[type="submit"]'):
                return {
                    'by': 'CSS_SELECTOR',
                    'value': 'button[type="submit"]',
                    'confidence': 'high',
                    'reasoning': 'Found submit button using type attribute'
                }

        if 'logout' in description_lower:
            if self._element_exists(driver, 'css selector', 'a.button.secondary'):
                return {
                    'by': 'CSS_SELECTOR',
                    'value': 'a.button.secondary',
                    'confidence': 'high',
                    'reasoning': 'Found logout button with class "button secondary"'
                }

        if 'flash' in description_lower or 'message' in description_lower:
            if self._element_exists(driver, 'id', 'flash'):
                return {
                    'by': 'ID',
                    'value': 'flash',
                    'confidence': 'high',
                    'reasoning': 'Found flash message container with id="flash"'
                }

        # Strategy 2: Try common ID patterns based on old value
        old_value = locator.value.lower()

        # Try removing trailing/leading characters
        if len(old_value) > 2:
            # Try adding common endings
            for suffix in ['', 's', 'e', 'name', 'field', 'input']:
                test_value = old_value + suffix
                if self._element_exists(driver, 'id', test_value):
                    return {
                        'by': 'ID',
                        'value': test_value,
                        'confidence': 'medium',
                        'reasoning': f'Found element with similar id="{test_value}" (added suffix)'
                    }

            # Try without last character
            test_value = old_value[:-1]
            if len(test_value) > 2 and self._element_exists(driver, 'id', test_value):
                return {
                    'by': 'ID',
                    'value': test_value,
                    'confidence': 'medium',
                    'reasoning': f'Found element with shorter id="{test_value}"'
                }

        # Strategy 3: Try common name attributes
        if locator.by == 'ID':
            # Try using name attribute instead
            if self._element_exists(driver, 'name', old_value):
                return {
                    'by': 'NAME',
                    'value': old_value,
                    'confidence': 'medium',
                    'reasoning': 'Element found using NAME attribute instead of ID'
                }

        print(f"   ⚠️  Mock healer couldn't determine correct locator")
        return None

    def _element_exists(self, driver, by, value):
        """Check if element exists on page"""
        try:
            if by == 'id':
                driver.find_element('id', value)
            elif by == 'name':
                driver.find_element('name', value)
            elif by == 'css selector':
                driver.find_element('css selector', value)
            elif by == 'xpath':
                driver.find_element('xpath', value)
            return True
        except:
            return False

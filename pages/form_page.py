# ==============================================================================
# PAGES DIRECTORY FILES
# ==============================================================================

# ------------------------------------------------------------------------------
# FILE: pages/__init__.py
# ------------------------------------------------------------------------------
"""Page Object Models package"""

from .base_page import BasePage
from .login_page import LoginPage
# from .form_page import FormPage

__all__ = ["BasePage", "LoginPage", "FormPage"]

# ------------------------------------------------------------------------------
# FILE: pages/base_page.py
# ------------------------------------------------------------------------------
"""Base page class for all page objects"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base page object class with common functionality"""

    def __init__(self, driver, smart_finder):
        """
        Initialize base page

        Args:
            driver: Selenium WebDriver instance
            smart_finder: SmartElementFinder instance
        """
        self.driver = driver
        self.smart_finder = smart_finder
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        print(f"📍 Navigated to: {url}")

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            return True
        except TimeoutException:
            return False

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        print("🔄 Page refreshed")

    def go_back(self):
        """Navigate back"""
        self.driver.back()
        print("⬅️  Navigated back")

    def take_screenshot(self, name):
        """Take screenshot"""
        from framework.utils import take_screenshot
        return take_screenshot(self.driver, name)

    def scroll_to_element(self, element):
        """Scroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_page_source(self):
        """Get page source"""
        return self.driver.page_source


# ------------------------------------------------------------------------------
# FILE: pages/login_page.py
# ------------------------------------------------------------------------------
"""Login page object"""

import time
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page object with smart locators"""

    def __init__(self, driver, smart_finder):
        super().__init__(driver, smart_finder)
        self.url = "https://the-internet.herokuapp.com/login"

    def open(self):
        """Open login page"""
        self.navigate_to(self.url)
        return self

    def enter_username(self, username):
        """
        Enter username

        Args:
            username: Username to enter
        """
        field = self.smart_finder.find_element("login_username")
        field.clear()
        field.send_keys(username)
        print(f"✍️  Entered username: {username}")
        return self

    def enter_password(self, password):
        """
        Enter password

        Args:
            password: Password to enter
        """
        field = self.smart_finder.find_element("login_password")
        field.clear()
        field.send_keys(password)
        print("✍️  Entered password: ********")
        return self

    def click_submit(self):
        """Click submit button"""
        button = self.smart_finder.find_element("login_submit")
        button.click()
        print("🖱️  Clicked submit button")
        time.sleep(1)  # Wait for page transition
        return self

    def login(self, username, password):
        """
        Complete login process

        Args:
            username: Username
            password: Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_flash_message(self):
        """Get flash message text"""
        message = self.smart_finder.find_element("login_flash_message")
        text = message.text
        print(f"💬 Flash message: {text}")
        return text

    def is_login_successful(self):
        """Check if login was successful"""
        current_url = self.get_current_url()
        is_successful = "secure" in current_url.lower()
        if is_successful:
            print("✅ Login successful - on secure page")
        else:
            print("❌ Login failed - not on secure page")
        return is_successful

    def is_error_displayed(self):
        """Check if error message is displayed"""
        try:
            message = self.get_flash_message()
            return "invalid" in message.lower() or "incorrect" in message.lower()
        except:
            return False

    def logout(self):
        """Logout from secure area"""
        try:
            logout_btn = self.smart_finder.find_element("logout_button")
            logout_btn.click()
            print("👋 Logged out")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"⚠️  Logout failed: {str(e)}")
            return False


# ------------------------------------------------------------------------------
# FILE: pages/form_page.py
# ------------------------------------------------------------------------------
"""Form page object"""

import time
from .base_page import BasePage
from selenium.webdriver.support.ui import Select


class FormPage(BasePage):
    """Generic form page object"""

    def __init__(self, driver, smart_finder):
        super().__init__(driver, smart_finder)

    def select_dropdown_by_text(self, locator_name, text):
        """
        Select dropdown option by visible text

        Args:
            locator_name: Name of the dropdown locator
            text: Visible text to select
        """
        element = self.smart_finder.find_element(locator_name)
        select = Select(element)
        select.select_by_visible_text(text)
        print(f"📝 Selected '{text}' from dropdown: {locator_name}")
        return self

    def select_dropdown_by_value(self, locator_name, value):
        """Select dropdown option by value"""
        element = self.smart_finder.find_element(locator_name)
        select = Select(element)
        select.select_by_value(value)
        print(f"📝 Selected value '{value}' from dropdown: {locator_name}")
        return self

    def select_dropdown_by_index(self, locator_name, index):
        """Select dropdown option by index"""
        element = self.smart_finder.find_element(locator_name)
        select = Select(element)
        select.select_by_index(index)
        print(f"📝 Selected index {index} from dropdown: {locator_name}")
        return self

    def get_selected_dropdown_text(self, locator_name):
        """Get currently selected dropdown text"""
        element = self.smart_finder.find_element(locator_name)
        select = Select(element)
        return select.first_selected_option.text

    def check_checkbox(self, locator_name):
        """
        Check a checkbox

        Args:
            locator_name: Name of the checkbox locator
        """
        element = self.smart_finder.find_element(locator_name)
        if not element.is_selected():
            element.click()
            print(f"☑️  Checked checkbox: {locator_name}")
        else:
            print(f"ℹ️  Checkbox already checked: {locator_name}")
        return self

    def uncheck_checkbox(self, locator_name):
        """
        Uncheck a checkbox

        Args:
            locator_name: Name of the checkbox locator
        """
        element = self.smart_finder.find_element(locator_name)
        if element.is_selected():
            element.click()
            print(f"☐ Unchecked checkbox: {locator_name}")
        else:
            print(f"ℹ️  Checkbox already unchecked: {locator_name}")
        return self

    def is_checkbox_checked(self, locator_name):
        """Check if checkbox is selected"""
        element = self.smart_finder.find_element(locator_name)
        return element.is_selected()

    def enter_text(self, locator_name, text):
        """
        Enter text into input field

        Args:
            locator_name: Name of the input locator
            text: Text to enter
        """
        element = self.smart_finder.find_element(locator_name)
        element.clear()
        element.send_keys(text)
        print(f"✍️  Entered text into {locator_name}: {text}")
        return self

    def clear_field(self, locator_name):
        """Clear input field"""
        element = self.smart_finder.find_element(locator_name)
        element.clear()
        print(f"🗑️  Cleared field: {locator_name}")
        return self

    def get_field_value(self, locator_name):
        """Get value from input field"""
        element = self.smart_finder.find_element(locator_name)
        return element.get_attribute("value")

    def click_button(self, locator_name):
        """
        Click a button

        Args:
            locator_name: Name of the button locator
        """
        button = self.smart_finder.find_element(locator_name)
        button.click()
        print(f"🖱️  Clicked button: {locator_name}")
        time.sleep(0.5)
        return self

    def upload_file(self, locator_name, file_path):
        """
        Upload a file

        Args:
            locator_name: Name of the file input locator
            file_path: Path to file to upload
        """
        element = self.smart_finder.find_element(locator_name)
        element.send_keys(file_path)
        print(f"📤 Uploaded file: {file_path}")
        return self

    def select_radio_button(self, locator_name):
        """Select a radio button"""
        element = self.smart_finder.find_element(locator_name)
        if not element.is_selected():
            element.click()
            print(f"🔘 Selected radio button: {locator_name}")
        return self

    def is_element_visible(self, locator_name):
        """Check if element is visible"""
        try:
            element = self.smart_finder.find_element(locator_name)
            return element.is_displayed()
        except:
            return False

    def is_element_enabled(self, locator_name):
        """Check if element is enabled"""
        try:
            element = self.smart_finder.find_element(locator_name)
            return element.is_enabled()
        except:
            return False
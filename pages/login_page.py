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
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
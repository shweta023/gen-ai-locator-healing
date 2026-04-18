"""Utility functions for the framework"""

import os
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def setup_chrome_driver(headless: bool = True, download_dir: str = None):
    """
    Setup Chrome WebDriver with common options

    Args:
        headless: Run in headless mode
        download_dir: Custom download directory

    Returns:
        WebDriver instance
    """
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument('--headless=new')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if download_dir:
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)

    # Use webdriver-manager to auto-download chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    return driver


def take_screenshot(driver, name: str, directory: str = "screenshots"):
    """Take and save screenshot"""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(directory, filename)
    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {filepath}")
    return filepath


def log_message(message: str, level: str = "INFO"):
    """Log formatted message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")
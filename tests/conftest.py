"""Pytest configuration and fixtures"""

import pytest
from dotenv import load_dotenv
from framework import LocatorRegistry, SmartElementFinder
from framework.utils import take_screenshot
from pages.login_page import LoginPage
from pages.form_page import FormPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def locator_registry():
    """Initialize locator registry for all tests"""
    registry = LocatorRegistry("config/locators.json")
    print(f"\n📋 Loaded {len(registry.locators)} locators from registry")
    yield registry


# @pytest.fixture(scope="session")
# def genai_healer():
#     """Initialize GenAI healer for all tests"""
#     api_key = os.getenv("ANTHROPIC_API_KEY")
#     healer = GenAILocatorHealer(api_key=api_key)
#     yield healer


@pytest.fixture(scope="session")
def genai_healer():
    """Initialize GenAI healer - uses mock if no API key"""

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Use mock if no valid API key
    if not api_key or api_key == "your-api-key-here":
        print("⚠️  No valid API key - using Mock GenAI Healer (no API calls)")
        from mock_genai_healer import MockGenAILocatorHealer
        healer = MockGenAILocatorHealer()
    else:
        print("✅ Using real GenAI Healer with API")
        from framework import GenAILocatorHealer
        healer = GenAILocatorHealer(api_key)

    yield healer


@pytest.fixture(scope="function")
def driver(request):
    """Initialize Chrome driver for each test"""
    headless = os.getenv("HEADLESS_MODE", "false").lower() == "false"
    # driver = setup_chrome_driver(headless=headless)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')

    # Use local ChromeDriver
    service = Service(
        executable_path=r"C:\Users\ShwetaSharma\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    print(f"\n🌐 Browser started (headless={headless})")

    yield driver

    # Teardown: take screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        take_screenshot(driver, f"failed_{test_name}")
        print(f"📸 Failure screenshot saved for: {test_name}")

    driver.quit()
    print("🔒 Browser closed")


@pytest.fixture(scope="function")
def smart_finder(driver, locator_registry, genai_healer):
    """Initialize smart element finder for each test"""
    auto_heal = os.getenv("AUTO_HEAL_ENABLED", "true").lower() == "true"
    max_attempts = int(os.getenv("MAX_HEAL_ATTEMPTS", "3"))

    finder = SmartElementFinder(
        driver,
        locator_registry,
        genai_healer,
        auto_heal=auto_heal,
        max_heal_attempts=max_attempts
    )

    yield finder

    # Print healing report after each test if healings occurred
    if finder.healing_log:
        print("\n" + "=" * 70)
        print("🏥 HEALING OCCURRED IN THIS TEST")
        print("=" * 70)
        finder.print_healing_report()


@pytest.fixture(scope="function")
def login_page(driver, smart_finder):
    """Initialize login page object"""
    return LoginPage(driver, smart_finder)


@pytest.fixture(scope="function")
def form_page(driver, smart_finder):
    """Initialize form page object"""
    return FormPage(driver, smart_finder)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to make test results available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Setup before all tests"""
    print("\n" + "=" * 70)
    print("🚀 GenAI Locator Healing Framework - Test Session Started")
    print("=" * 70)

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✅ Anthropic API key found - GenAI healing enabled")
    else:
        print("⚠️  Anthropic API key not found - GenAI healing disabled")
        print("   Set ANTHROPIC_API_KEY in .env file to enable healing")

    # Check other config
    headless = os.getenv("HEADLESS_MODE", "false")
    auto_heal = os.getenv("AUTO_HEAL_ENABLED", "true")
    print(f"⚙️  Configuration:")
    print(f"   - Headless Mode: {headless}")
    print(f"   - Auto Healing: {auto_heal}")
    print(f"   - Max Heal Attempts: {os.getenv('MAX_HEAL_ATTEMPTS', '3')}")

    yield

    print("\n" + "=" * 70)
    print("✅ Test Session Complete")
    print("=" * 70)


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for basic functionality"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression test suite"
    )
    config.addinivalue_line(
        "markers", "healing: Tests focused on locator healing functionality"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )

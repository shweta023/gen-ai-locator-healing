"""
Demo tests for login functionality with auto-healing

This module contains comprehensive login tests demonstrating:
- Successful login scenarios
- Failed login scenarios (invalid credentials)
- Logout functionality
- Page object pattern usage
- Smart locator auto-healing
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLoginDemo:
    """Test login functionality with smart locators and auto-healing"""

    @pytest.mark.smoke
    def test_successful_login(self, driver, smart_finder):
        """
        Test successful login with correct credentials
        """
        print("\n" + "="*70)
        print("🧪 TEST: Successful Login with Valid Credentials")
        print("="*70)

        # Navigate to login page
        driver.get("https://the-internet.herokuapp.com/login")
        print("📍 Navigated to: https://the-internet.herokuapp.com/login")
        time.sleep(1)

        # Find elements using smart finder (auto-heals if needed)
        print("\n🔍 Finding form elements...")
        username_field = smart_finder.find_element("login_username")
        password_field = smart_finder.find_element("login_password")
        submit_button = smart_finder.find_element("login_submit")

        # Perform login
        print("\n📝 Filling login form...")
        username_field.clear()
        username_field.send_keys("tomsmith")
        print("   ✅ Entered username: tomsmith")

        password_field.clear()
        password_field.send_keys("SuperSecretPassword!")
        print("   ✅ Entered password: ********")

        submit_button.click()
        print("   ✅ Clicked submit button")

        # Wait for page transition
        time.sleep(2)

        # Verify success - URL should contain "secure"
        current_url = driver.current_url
        print(f"\n🌐 Current URL: {current_url}")
        assert "secure" in current_url.lower(), f"Login failed - URL is {current_url}"
        print("✅ SUCCESS: Redirected to secure page")

        # Verify flash message
        flash_message = smart_finder.find_element("login_flash_message")
        message_text = flash_message.text
        print(f"💬 Flash message: {message_text}")

        assert "You logged into a secure area!" in message_text, \
            f"Expected success message, got: {message_text}"
        print("✅ SUCCESS: Correct flash message displayed")

        print("\n" + "="*70)
        print("✅ TEST PASSED: Login successful!")
        print("="*70)

    @pytest.mark.smoke
    def test_failed_login_invalid_password(self, driver, smart_finder):
        """
        Test failed login with invalid password

        Steps:
        1. Navigate to login page
        2. Enter valid username
        3. Enter invalid password
        4. Click submit
        5. Verify stays on login page
        6. Verify error message
        """
        print("\n" + "="*70)
        print("🧪 TEST: Failed Login with Invalid Password")
        print("="*70)

        driver.get("https://the-internet.herokuapp.com/login")
        print("📍 Navigated to login page")
        time.sleep(1)

        # Find form elements
        print("\n🔍 Finding form elements...")
        username_field = smart_finder.find_element("login_username")
        password_field = smart_finder.find_element("login_password")
        submit_button = smart_finder.find_element("login_submit")

        # Enter invalid credentials
        print("\n📝 Filling form with invalid password...")
        username_field.clear()
        username_field.send_keys("tomsmith")
        print("   ✅ Entered username: tomsmith")

        password_field.clear()
        password_field.send_keys("wrongpassword123")
        print("   ✅ Entered password: wrongpassword123 (invalid)")

        submit_button.click()
        print("   ✅ Clicked submit button")

        time.sleep(1)

        # Should still be on login page
        current_url = driver.current_url
        print(f"\n🌐 Current URL: {current_url}")
        assert "login" in current_url.lower(), \
            f"Should stay on login page, but URL is {current_url}"
        print("✅ SUCCESS: Stayed on login page as expected")

        # Verify error message
        flash_message = smart_finder.find_element("login_flash_message")
        message_text = flash_message.text
        print(f"💬 Flash message: {message_text}")

        assert "Your password is invalid!" in message_text, \
            f"Expected password error, got: {message_text}"
        print("✅ SUCCESS: Correct error message displayed")

        print("\n" + "="*70)
        print("✅ TEST PASSED: Invalid password handled correctly!")
        print("="*70)

    @pytest.mark.smoke
    def test_failed_login_invalid_username(self, driver, smart_finder):
        """
        Test failed login with invalid username

        Steps:
        1. Navigate to login page
        2. Enter invalid username
        3. Enter valid password
        4. Click submit
        5. Verify error message for username
        """
        print("\n" + "="*70)
        print("🧪 TEST: Failed Login with Invalid Username")
        print("="*70)

        driver.get("https://the-internet.herokuapp.com/login")
        print("📍 Navigated to login page")
        time.sleep(1)

        # Find form elements
        print("\n🔍 Finding form elements...")
        username_field = smart_finder.find_element("login_username")
        password_field = smart_finder.find_element("login_password")
        submit_button = smart_finder.find_element("login_submit")

        # Enter invalid credentials
        print("\n📝 Filling form with invalid username...")
        username_field.clear()
        username_field.send_keys("invaliduser")
        print("   ✅ Entered username: invaliduser (invalid)")

        password_field.clear()
        password_field.send_keys("SuperSecretPassword!")
        print("   ✅ Entered password: ********")

        submit_button.click()
        print("   ✅ Clicked submit button")

        time.sleep(1)

        # Verify error message
        flash_message = smart_finder.find_element("login_flash_message")
        message_text = flash_message.text
        print(f"💬 Flash message: {message_text}")

        assert "Your username is invalid!" in message_text, \
            f"Expected username error, got: {message_text}"
        print("✅ SUCCESS: Correct error message displayed")

        print("\n" + "="*70)
        print("✅ TEST PASSED: Invalid username handled correctly!")
        print("="*70)


    # @pytest.mark.smoke
    # def test_logout(self, driver, smart_finder):
    #     """
    #     Test logout functionality
    #
    #     Steps:
    #     1. Login first with valid credentials
    #     2. Verify login successful
    #     3. Click logout button
    #     4. Verify redirected back to login page
    #     5. Verify logout flash message
    #     """
    #     print("\n" + "="*70)
    #     print("🧪 TEST: Logout Functionality")
    #     print("="*70)
    #
    #     # First login
    #     print("\n🔐 Step 1: Logging in...")
    #     driver.get("https://the-internet.herokuapp.com/login")
    #     time.sleep(1)
    #
    #     username_field = smart_finder.find_element("login_username")
    #     password_field = smart_finder.find_element("login_password")
    #     submit_button = smart_finder.find_element("login_submit")
    #
    #     username_field.send_keys("tomsmith")
    #     password_field.send_keys("SuperSecretPassword!")
    #     submit_button.click()
    #     print("   ✅ Login form submitted")
    #
    #     time.sleep(2)
    #
    #     # Verify login
    #     current_url = driver.current_url
    #     assert "secure" in current_url.lower(), f"Login failed, URL: {current_url}"
    #     print("   ✅ Login successful - on secure page")
    #
    #     # Now logout
    #     print("\n👋 Step 2: Logging out...")
    #     logout_button = smart_finder.find_element("logout_button")
    #     logout_button.click()
    #     print("   ✅ Clicked logout button")
    #
    #     time.sleep(1)
    #
    #     # Should be back on login page
    #     current_url = driver.current_url
    #     print(f"\n🌐 Current URL: {current_url}")
    #     assert "login" in current_url.lower(), \
    #         f"Should return to login page, but URL is {current_url}"
    #     print("✅ SUCCESS: Redirected back to login page")
    #
    #     # Verify logout message
    #     flash_message = smart_finder.find_element("login_flash_message")
    #     message_text = flash_message.text
    #     print(f"💬 Flash message: {message_text}")
    #
    #     assert "You logged out of the secure area!" in message_text, \
    #         f"Expected logout message, got: {message_text}"
    #     print("✅ SUCCESS: Logout message displayed")
    #
    #     print("\n" + "="*70)
    #     print("✅ TEST PASSED: Logout successful!")
    #     print("="*70)


    def test_empty_credentials(self, driver, smart_finder):
        """
        Test login with empty credentials

        Steps:
        1. Navigate to login page
        2. Click submit without entering any credentials
        3. Verify error message displayed
        """
        print("\n" + "="*70)
        print("🧪 TEST: Login with Empty Credentials")
        print("="*70)

        driver.get("https://the-internet.herokuapp.com/login")
        print("📍 Navigated to login page")
        time.sleep(1)

        # Just click submit without entering anything
        print("\n📝 Submitting form with empty fields...")
        submit_button = smart_finder.find_element("login_submit")
        submit_button.click()
        print("   ✅ Clicked submit with empty fields")

        time.sleep(1)

        # Should show error
        flash_message = smart_finder.find_element("login_flash_message")
        message_text = flash_message.text
        print(f"💬 Flash message: {message_text}")

        assert "Your username is invalid!" in message_text, \
            f"Expected empty credentials error, got: {message_text}"
        print("✅ SUCCESS: Error message for empty credentials")

        print("\n" + "="*70)
        print("✅ TEST PASSED: Empty credentials validation works!")
        print("="*70)

    def test_empty_password(self, driver, smart_finder):
        """
        Test login with empty password

        Steps:
        1. Navigate to login page
        2. Enter username only
        3. Leave password empty
        4. Click submit
        5. Verify error message
        """
        print("\n" + "="*70)
        print("🧪 TEST: Login with Empty Password")
        print("="*70)

        driver.get("https://the-internet.herokuapp.com/login")
        print("📍 Navigated to login page")
        time.sleep(1)

        print("\n📝 Filling username only...")
        username_field = smart_finder.find_element("login_username")
        submit_button = smart_finder.find_element("login_submit")

        username_field.send_keys("tomsmith")
        print("   ✅ Entered username: tomsmith")
        print("   ⚠️  Leaving password empty")

        submit_button.click()
        print("   ✅ Clicked submit")

        time.sleep(1)

        # Should show error
        flash_message = smart_finder.find_element("login_flash_message")
        message_text = flash_message.text
        print(f"💬 Flash message: {message_text}")

        assert "invalid" in message_text.lower(), \
            f"Expected error message, got: {message_text}"
        print("✅ SUCCESS: Error message for empty password")

        print("\n" + "="*70)
        print("✅ TEST PASSED: Empty password validation works!")
        print("="*70)


# def test_healing_debug(driver, smart_finder):
#     driver.get("https://the-internet.herokuapp.com/login")
#     time.sleep(2)
#
#     print(f"\n🔍 Auto-heal: {smart_finder.auto_heal}")
#     print(f"🔍 Max attempts: {smart_finder.max_heal_attempts}")
#     print(f"🔍 GenAI client: {smart_finder.healer.client is not None}")
#
#     try:
#         element = smart_finder.find_element("login_username", timeout=15)
#         print("✅ Found (may have healed)")
#     except Exception as e:
#         print(f"❌ Failed: {e}")
#         print(f"Healing log: {len(smart_finder.healing_log)} attempts")

'''
def test_healing_with_full_visibility(driver, locator_registry, genai_healer):
    """Test with maximum visibility to see healing in action"""
    from framework import SmartElementFinder

    print("\n" + "=" * 80)
    print("🔍 HEALING VISIBILITY TEST")
    print("=" * 80)

    smart_finder = SmartElementFinder(
        driver, locator_registry, genai_healer,
        auto_heal=True, max_heal_attempts=5, verbose=True
    )

    driver.get("https://the-internet.herokuapp.com/login")
    time.sleep(2)

    locator = locator_registry.get_locator("login_username")
    print(f"\nCurrent locator value: '{locator.value}'")

    try:
        element = smart_finder.find_element("login_username", timeout=10)
        print(f"\n✅ ELEMENT FOUND!")

        # Check if healed
        new_locator = locator_registry.get_locator("login_username")
        if new_locator.value != locator.value:
            print(f"🎉 HEALING WORKED: '{locator.value}' → '{new_locator.value}'")
    except Exception as e:
        print(f"\n❌ FAILED: {e}")

    # Show healing log
    healing_log = smart_finder.get_healing_report()
    print(f"\nHealing attempts: {len(healing_log)}")
    for entry in healing_log:
        print(f"  - {entry['old_value']} → {entry['new_value']}")
        
'''


if __name__ == "__main__":
    """
    Allow running this test file directly
    """
    pytest.main([__file__, "-v", "-s"])
"""Demo tests for form functionality"""

import pytest
import time
import os
import tempfile
from selenium.webdriver.support.ui import Select


class TestFormDemo:
    """Test various form interactions"""

    def test_dropdown_selection(self, driver):
        """Test dropdown selection"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Dropdown Selection")
        print("=" * 70)

        driver.get("https://the-internet.herokuapp.com/dropdown")
        time.sleep(1)

        # Find dropdown
        dropdown = driver.find_element("id", "dropdown")
        select = Select(dropdown)

        # Initially Option 1 might be selected, let's select Option 2
        print("📝 Selecting Option 2...")
        select.select_by_visible_text("Option 2")
        time.sleep(1)

        # Verify selection
        selected_option = select.first_selected_option
        assert selected_option.text == "Option 2"
        print(f"✅ SUCCESS: Selected option is: {selected_option.text}")

        # Select Option 1
        print("📝 Selecting Option 1...")
        select.select_by_index(1)
        time.sleep(1)

        selected_option = select.first_selected_option
        assert selected_option.text == "Option 1"
        print(f"✅ SUCCESS: Selected option is: {selected_option.text}")

        print("\n✅ TEST PASSED: Dropdown selection works!")

    def test_checkboxes(self, driver):
        """Test checkbox interactions"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Checkbox Interactions")
        print("=" * 70)

        driver.get("https://the-internet.herokuapp.com/checkboxes")
        time.sleep(1)

        checkboxes = driver.find_elements("css selector", "input[type='checkbox']")
        print(f"📝 Found {len(checkboxes)} checkboxes")

        # Check initial states
        initial_states = [cb.is_selected() for cb in checkboxes]
        print(f"   Initial states: {initial_states}")

        # Check all checkboxes
        for i, checkbox in enumerate(checkboxes):
            if not checkbox.is_selected():
                checkbox.click()
                print(f"   ☑️  Checked checkbox {i + 1}")
            else:
                print(f"   ℹ️  Checkbox {i + 1} already checked")

        time.sleep(1)

        # Verify all are checked
        checkboxes = driver.find_elements("css selector", "input[type='checkbox']")
        for i, checkbox in enumerate(checkboxes):
            assert checkbox.is_selected(), f"Checkbox {i + 1} should be checked"

        print("✅ SUCCESS: All checkboxes are checked")

        # Uncheck all
        for i, checkbox in enumerate(checkboxes):
            checkbox.click()
            print(f"   ☐ Unchecked checkbox {i + 1}")

        time.sleep(1)

        # Verify all are unchecked
        checkboxes = driver.find_elements("css selector", "input[type='checkbox']")
        for i, checkbox in enumerate(checkboxes):
            assert not checkbox.is_selected(), f"Checkbox {i + 1} should be unchecked"

        print("✅ SUCCESS: All checkboxes are unchecked")
        print("\n✅ TEST PASSED: Checkbox interactions work!")

    def test_file_upload(self, driver):
        """Test file upload"""
        print("\n" + "=" * 70)
        print("🧪 TEST: File Upload")
        print("=" * 70)

        driver.get("https://the-internet.herokuapp.com/upload")
        time.sleep(1)

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for upload testing.\n")
            f.write("GenAI Locator Healing Framework Demo\n")
            temp_file_path = f.name

        print(f"📄 Created temporary file: {temp_file_path}")

        try:
            # Upload file
            file_input = driver.find_element("id", "file-upload")
            file_input.send_keys(temp_file_path)
            print("📤 File selected for upload")

            submit_button = driver.find_element("id", "file-submit")
            submit_button.click()
            print("🖱️  Clicked upload button")

            time.sleep(2)

            # Verify upload
            uploaded_files = driver.find_element("id", "uploaded-files")
            uploaded_filename = uploaded_files.text

            assert len(uploaded_filename) > 0, "No file was uploaded"
            print(f"✅ SUCCESS: File uploaded: {uploaded_filename}")

            # Verify we're on success page
            assert "file-uploaded" in driver.current_url or "upload" in driver.page_source.lower()
            print("✅ SUCCESS: Upload confirmed")

        finally:
            # Cleanup
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                print(f"🗑️  Cleaned up temporary file")

        print("\n✅ TEST PASSED: File upload works!")

    def test_input_field(self, driver):
        """Test input field interactions"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Input Field Interactions")
        print("=" * 70)

        driver.get("https://the-internet.herokuapp.com/inputs")
        time.sleep(1)

        # Find input field
        input_field = driver.find_element("css selector", "input[type='number']")

        # Test entering numbers
        test_value = "12345"
        input
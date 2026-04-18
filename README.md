# GenAI Locator Healing Framework

## Overview

The **GenAI Locator Healing Framework** is a Selenium-based automation framework enhanced with GenAI capabilities to auto-heal broken locators. It leverages Anthropic's Claude AI to suggest and update locators dynamically, ensuring robust and resilient test automation.

---

## Features

- **GenAI-Powered Locator Healing**: Automatically detects and fixes broken locators using AI.
- **Smart Element Finder**: Enhanced Selenium element finder with auto-healing capabilities.
- **Locator Registry**: Centralized management of locators with versioning and failure tracking.
- **Mock GenAI Healer**: Simulates GenAI behavior for testing without an API key.
- **Page Object Model (POM)**: Organized structure for scalable and maintainable tests.
- **Comprehensive Test Suite**: Includes tests for login, forms, dropdowns, checkboxes, and file uploads.

---

## Prerequisites

- **Python**: Version 3.8 or higher
- **Chrome Browser**: Latest version
- **ChromeDriver**: Managed automatically via `webdriver-manager`

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd genai-locator-healing
   

1. Create and activate a virtual environment:  
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install dependencies:  
pip install -r requirements.txt
3. (Optional) Install development dependencies:  
pip install black flake8 mypy pytest-cov
<hr></hr>

Configuration

Environment Variables
ANTHROPIC_API_KEY: Set this environment variable to enable GenAI-powered locator healing.
Example: export ANTHROPIC_API_KEY="your-api-key"

Locator Registry
Locators are managed in config/locators.json. A backup file (locators.backup.json) is maintained automatically.

Usage

Running Tests
1.Run all tests:  
pytest -v
2.Run specific tests:  
pytest tests/test_login_demo.py::TestLoginDemo::test_successful_login
Generate an HTML report:
pytest --html=report.html

Auto-Healing
The SmartElementFinder automatically attempts to heal broken locators using GenAI. Healing logs are printed during test execution.

Project Structure

genai-locator-healing/
├── config/
│   ├── locators.json
│   └── locators.backup.json
├── framework/
│   ├── genai_healer.py
│   ├── locator_registry.py
│   ├── smart_finder.py
│   └── utils.py
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   ├── test_login_demo.py
│   └── test_form_demo.py
├── requirements.txt
├── setup.py
└── README.md

Key Components
Locator Registry
-Centralized storage for locators with metadata (e.g., by, value, description, failure_count).
-Automatically updates locators when healed.

GenAI Healer
-Uses Anthropic's Claude AI to analyze page HTML and suggest new locators.
-Mock implementation available for testing without an API key.

Smart Element Finder
-Enhanced Selenium element finder with:
    -Auto-healing capabilities
    -Detailed logging
    -Support for retries and failure tracking


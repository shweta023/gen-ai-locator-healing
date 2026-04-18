"""GenAI-powered locator healing using Claude AI"""

import os
import json
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from .locator_registry import LocatorConfig


class GenAILocatorHealer:
    """Uses GenAI to detect and fix broken locators"""

    def __init__(self, api_key: str = None):
        # Use environment variable or provided key
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("✅ GenAI Healer initialized with API key")
            except ImportError:
                print("❌ anthropic package not installed. Run: pip install anthropic")
            except Exception as e:
                print(f"❌ Error initializing GenAI: {str(e)}")
        else:
            print("⚠️  No Anthropic API key found. Set ANTHROPIC_API_KEY environment variable.")
            print("   GenAI healing will be disabled.")

    def analyze_page_and_suggest_locator(
            self,
            driver: webdriver.Chrome,
            broken_locator: LocatorConfig,
            page_source: str = None
    ) -> Optional[Dict[str, str]]:
        """
        Analyze page HTML and suggest a new locator using GenAI

        Args:
            driver: Selenium WebDriver instance
            broken_locator: The locator that failed
            page_source: Optional page source (will be fetched if not provided)

        Returns:
            Dict with 'by', 'value', 'confidence', 'reasoning' keys, or None
        """
        if not self.client:
            print("❌ GenAI healing not available (no API key or client)")
            return None

        try:
            # Get page source if not provided
            if not page_source:
                page_source = driver.page_source

            # Extract relevant HTML snippet
            html_snippet = self._extract_relevant_html(page_source, broken_locator)

            # Get current URL for context
            current_url = driver.current_url

            prompt = self._build_prompt(broken_locator, html_snippet, current_url)

            print(f"🤖 Asking GenAI to analyze locator: {broken_locator.name}")

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON response
            content = response.content[0].text
            suggestion = self._parse_ai_response(content)

            if suggestion:
                print(f"✅ GenAI Suggestion:")
                print(f"   Strategy: {suggestion['by']}")
                print(f"   Value: {suggestion['value']}")
                print(f"   Confidence: {suggestion['confidence']}")
                print(f"   Reasoning: {suggestion['reasoning']}")

            return suggestion

        except Exception as e:
            print(f"❌ GenAI analysis failed: {str(e)}")
            return None

    def _build_prompt(self, locator: LocatorConfig, html: str, url: str) -> str:
        """Build prompt for GenAI"""
        return f"""You are a Selenium test automation expert. A locator has broken and needs to be fixed.

CURRENT PAGE URL:
{url}

BROKEN LOCATOR DETAILS:
- Name: {locator.name}
- Description: {locator.description}
- Page: {locator.page}
- Old Strategy: {locator.by}
- Old Value: {locator.value}
- Failure Count: {locator.failure_count}

CURRENT PAGE HTML SNIPPET:
```html
{html}
```

TASK:
Analyze the HTML and suggest the BEST new locator strategy to find the element described as "{locator.description}".

REQUIREMENTS:
1. Prefer strategies in this order: ID > Name > CSS Selector > XPath
2. Locator should be stable and resilient to minor UI changes
3. Avoid overly complex XPath with absolute paths or indices
4. Consider test-friendly attributes: data-testid, data-qa, aria-label, role
5. For buttons: look for type, class, text content
6. For inputs: look for id, name, type, placeholder

RESPOND ONLY WITH A JSON OBJECT (no markdown, no code blocks):
{{
    "by": "ID|NAME|CSS_SELECTOR|XPATH",
    "value": "the_locator_value",
    "confidence": "high|medium|low",
    "reasoning": "brief explanation of why this locator is better"
}}"""

    def _parse_ai_response(self, content: str) -> Optional[Dict]:
        """Parse AI response and extract JSON"""
        try:
            # Remove markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            # Parse JSON
            suggestion = json.loads(content.strip())

            # Validate required fields
            required_fields = ['by', 'value', 'confidence', 'reasoning']
            if all(field in suggestion for field in required_fields):
                return suggestion
            else:
                print(f"⚠️  Invalid AI response: missing required fields")
                return None

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse AI response as JSON: {str(e)}")
            print(f"   Response: {content[:200]}")
            return None

    def _extract_relevant_html(
            self,
            page_source: str,
            locator: LocatorConfig,
            max_lines: int = 100
    ) -> str:
        """Extract relevant portion of HTML"""
        lines = page_source.split('\n')

        # Try to find lines mentioning keywords from description
        keywords = locator.description.lower().split()
        # Add locator value keywords
        keywords.extend(locator.value.lower().split())

        relevant_sections = []

        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords if len(keyword) > 3):
                # Found relevant line, get context around it
                start = max(0, i - 20)
                end = min(len(lines), i + 20)
                section = '\n'.join(lines[start:end])
                relevant_sections.append(section)

                if len(relevant_sections) >= 2:  # Get max 2 sections
                    break

        if relevant_sections:
            result = '\n...\n'.join(relevant_sections)
        else:
            # If no keywords found, return body section
            body_start = page_source.lower().find('<body')
            if body_start != -1:
                body_section = page_source[body_start:body_start + 5000]
                result = body_section
            else:
                result = page_source[:5000]

        # Limit total length
        lines = result.split('\n')
        if len(lines) > max_lines:
            return '\n'.join(lines[:max_lines]) + '\n... (truncated)'

        return result

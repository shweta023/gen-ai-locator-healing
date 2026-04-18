"""Locator Registry for managing all element locators"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Optional


@dataclass
class LocatorConfig:
    """Configuration for a locator"""
    name: str
    by: str
    value: str
    description: str
    page: str
    last_updated: str = ""
    failure_count: int = 0


class LocatorRegistry:
    """Central registry for all locators"""

    def __init__(self, config_file: str = "config/locators.json"):
        self.config_file = config_file
        self.locators: Dict[str, LocatorConfig] = {}
        self.backup_file = config_file.replace('.json', '.backup.json')
        self.load_locators()

    def load_locators(self):
        """Load locators from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        self.locators[key] = LocatorConfig(**value)
                print(f"✅ Loaded {len(self.locators)} locators from {self.config_file}")
            except Exception as e:
                print(f"❌ Error loading locators: {str(e)}")
                self._initialize_default_locators()
        else:
            print(f"⚠️  Locator file not found, creating default: {self.config_file}")
            self._initialize_default_locators()

    def _initialize_default_locators(self):
        """Initialize with default locators"""
        self.locators = {
            "login_username": LocatorConfig(
                name="login_username",
                by="ID",
                value="username",
                description="Username input field on login page",
                page="login",
                last_updated=datetime.now().isoformat()
            ),
            "login_password": LocatorConfig(
                name="login_password",
                by="ID",
                value="password",
                description="Password input field on login page",
                page="login",
                last_updated=datetime.now().isoformat()
            ),
            "login_submit": LocatorConfig(
                name="login_submit",
                by="CSS_SELECTOR",
                value="button[type='submit']",
                description="Submit button on login page",
                page="login",
                last_updated=datetime.now().isoformat()
            ),
        }
        self.save_locators()

    def save_locators(self):
        """Save locators to JSON file"""
        try:
            # Create backup first
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    backup_data = f.read()
                with open(self.backup_file, 'w') as f:
                    f.write(backup_data)

            # Save new data
            data = {key: asdict(loc) for key, loc in self.locators.items()}

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Saved {len(self.locators)} locators to {self.config_file}")
        except Exception as e:
            print(f"❌ Error saving locators: {str(e)}")

    def get_locator(self, name: str) -> Optional[LocatorConfig]:
        """Get a locator by name"""
        return self.locators.get(name)

    def update_locator(self, name: str, new_value: str, by: Optional[str] = None):
        """Update a locator value"""
        if name in self.locators:
            old_value = self.locators[name].value
            self.locators[name].value = new_value
            if by:
                self.locators[name].by = by
            self.locators[name].last_updated = datetime.now().isoformat()
            self.locators[name].failure_count = 0
            self.save_locators()
            print(f"🔄 Updated locator '{name}': {old_value} → {new_value}")
        else:
            print(f"⚠️  Locator '{name}' not found in registry")

    def increment_failure(self, name: str):
        """Increment failure count for a locator"""
        if name in self.locators:
            self.locators[name].failure_count += 1
            self.save_locators()
            print(f"⚠️  Failure count for '{name}': {self.locators[name].failure_count}")

    def add_locator(self, locator: LocatorConfig):
        """Add a new locator to registry"""
        self.locators[locator.name] = locator
        self.save_locators()
        print(f"➕ Added new locator: {locator.name}")

    def get_all_locators(self) -> Dict[str, LocatorConfig]:
        """Get all locators"""
        return self.locators

    def get_locators_by_page(self, page: str) -> Dict[str, LocatorConfig]:
        """Get all locators for a specific page"""
        return {name: loc for name, loc in self.locators.items() if loc.page == page}
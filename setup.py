from setuptools import setup, find_packages

setup(
    name="genai-locator-healing",
    version="1.0.0",
    description="GenAI-powered locator healing framework for Selenium",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.15.2",
        "pytest>=7.4.3",
        "anthropic>=0.40.0",
        "webdriver-manager>=4.0.1",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
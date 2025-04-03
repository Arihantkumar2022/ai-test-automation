#!/usr/bin/env python3
"""
Utility functions for the AI-driven test automation project.
"""

import os
import sys
import re
from urllib.parse import urlparse

def setup_directories(output_dir):
    """
    Set up necessary directories for the project.
    
    Args:
        output_dir (str): The output directory path.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        os.makedirs(os.path.join(templates_dir, 'ai_prompts'))
        os.makedirs(os.path.join(templates_dir, 'export_templates'))
        
        # Create default prompt templates
        create_default_templates()

def create_default_templates():
    """Create default template files if they don't exist."""
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    
    # Create test case prompt template
    test_case_prompt_path = os.path.join(templates_dir, 'ai_prompts', 'test_case_prompt_template.txt')
    if not os.path.exists(test_case_prompt_path):
        with open(test_case_prompt_path, 'w', encoding='utf-8') as f:
            f.write("""I need to generate test cases for a website called "{site_name}" ({site_url}).
I've extracted the following UI elements from the site:

{elements_summary}

Based on these elements, please generate 3-5 comprehensive test cases that would effectively test the key functionality of this website.

For each test case, provide:
1. A Test Case ID and brief description
2. Steps to execute (numbered)
3. Expected results

Format each test case clearly, making sure each one tests a specific functionality of the website.
""")
    
    # Create test script prompt template
    test_script_prompt_path = os.path.join(templates_dir, 'ai_prompts', 'test_script_prompt_template.txt')
    if not os.path.exists(test_script_prompt_path):
        with open(test_script_prompt_path, 'w', encoding='utf-8') as f:
            f.write("""Please create a Python Selenium script for the following test case:

Test Case ID: {test_id}
Test Scenario: {test_scenario}

Steps to Execute:
{steps}

Expected Result:
{expected_result}

Generate a complete, executable Python script using Selenium WebDriver that follows these steps exactly. Include proper waits, assertions, and exception handling. The script should be well-commented and follow best practices for Selenium automation.

Please use the following imports and structure:
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest
import time

class TestCase(unittest.TestCase):
    def setUp(self):
        # Setup code here
        pass
        
    def tearDown(self):
        # Cleanup code here
        pass
        
    def test_scenario(self):
        # Test implementation here
        pass
        
if __name__ == "__main__":
    unittest.main()
```
""")

def load_template(template_name):
    """
    Load a template file.
    
    Args:
        template_name (str): Name of the template file.
        
    Returns:
        str: The template content.
    """
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    template_path = os.path.join(templates_dir, template_name)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        print("Creating default templates...")
        create_default_templates()
        
        # Try loading again
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

def get_user_input(prompt):
    """
    Get multi-line input from the user.
    
    Args:
        prompt (str): The prompt to display to the user.
        
    Returns:
        str: The user's input.
    """
    print(prompt)
    
    lines = []
    while True:
        try:
            line = input()
            if not line.strip() and lines and not lines[-1].strip():
                break
            lines.append(line)
        except EOFError:
            break
    
    return "\n".join(lines)

def validate_url(url):
    """
    Validate if a string is a proper URL.
    
    Args:
        url (str): The URL to validate.
        
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

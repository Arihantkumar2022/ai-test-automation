#!/usr/bin/env python3
"""
Element Extractor module for web scraping and UI element extraction.
This module handles Task 1 of the project: extracting UI elements from a website.
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class ElementExtractor:
    """Class responsible for extracting UI elements from a website."""
    
    def __init__(self, url):
        """
        Initialize the ElementExtractor.
        
        Args:
            url (str): The URL of the website to scrape.
        """
        self.url = url
        
    def setup_driver(self):
        """Set up and return a Selenium WebDriver instance."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def extract_elements(self):
        """
        Extract UI elements from the target website.
        
        Returns:
            dict: A dictionary containing the extracted elements categorized by type.
        """
        driver = self.setup_driver()
        try:
            print(f"Navigating to {self.url}")
            driver.get(self.url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(('tag name', 'body'))
            )
            
            # Allow time for dynamic content to load
            time.sleep(3)
            
            # Get page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract elements by type
            elements = {
                'buttons': self._extract_buttons(soup),
                'links': self._extract_links(soup),
                'inputs': self._extract_inputs(soup),
                'forms': self._extract_forms(soup, driver)
            }
            
            # Add page metadata
            elements['metadata'] = {
                'title': driver.title,
                'url': driver.current_url,
                'page_structure': self._get_page_structure(soup)
            }
            
            return elements
            
        finally:
            driver.quit()
    
    def _extract_buttons(self, soup):
        """Extract button elements from the page."""
        buttons = []
        
        # Find all button tags
        button_tags = soup.find_all('button')
        for button in button_tags:
            button_info = {
                'element_type': 'button',
                'text': button.text.strip(),
                'id': button.get('id', ''),
                'class': ' '.join(button.get('class', [])),
                'name': button.get('name', ''),
                'disabled': button.has_attr('disabled'),
                'type': button.get('type', ''),
                'attributes': {k: v for k, v in button.attrs.items() if k not in ['id', 'class', 'name', 'type']}
            }
            buttons.append(button_info)
        
        # Find input elements of type button or submit
        input_buttons = soup.find_all('input', type=['button', 'submit', 'reset'])
        for button in input_buttons:
            button_info = {
                'element_type': 'input_button',
                'text': button.get('value', ''),
                'id': button.get('id', ''),
                'class': ' '.join(button.get('class', [])),
                'name': button.get('name', ''),
                'disabled': button.has_attr('disabled'),
                'type': button.get('type', ''),
                'attributes': {k: v for k, v in button.attrs.items() if k not in ['id', 'class', 'name', 'type', 'value']}
            }
            buttons.append(button_info)
            
        # Find elements with button-like class names
        button_classes = soup.find_all(class_=lambda c: c and ('btn' in c.lower() or 'button' in c.lower()))
        for element in button_classes:
            if element.name not in ['button', 'input']:  # Avoid duplicates
                button_info = {
                    'element_type': 'button_class',
                    'text': element.text.strip(),
                    'html_tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])),
                    'attributes': {k: v for k, v in element.attrs.items() if k not in ['id', 'class']}
                }
                buttons.append(button_info)
        
        return buttons
    
    def _extract_links(self, soup):
        """Extract link elements from the page."""
        links = []
        
        # Find all anchor tags
        anchor_tags = soup.find_all('a')
        for link in anchor_tags:
            link_info = {
                'element_type': 'link',
                'text': link.text.strip(),
                'href': link.get('href', ''),
                'id': link.get('id', ''),
                'class': ' '.join(link.get('class', [])),
                'name': link.get('name', ''),
                'title': link.get('title', ''),
                'target': link.get('target', ''),
                'attributes': {k: v for k, v in link.attrs.items() 
                              if k not in ['href', 'id', 'class', 'name', 'title', 'target']}
            }
            links.append(link_info)
        
        return links
    
    def _extract_inputs(self, soup):
        """Extract input fields from the page."""
        inputs = []
        
        # Find all input tags (excluding button/submit types which are handled as buttons)
        input_tags = soup.find_all('input', type=lambda t: t not in ['button', 'submit', 'reset'])
        for input_field in input_tags:
            input_info = {
                'element_type': 'input',
                'type': input_field.get('type', 'text'),
                'id': input_field.get('id', ''),
                'name': input_field.get('name', ''),
                'placeholder': input_field.get('placeholder', ''),
                'value': input_field.get('value', ''),
                'required': input_field.has_attr('required'),
                'class': ' '.join(input_field.get('class', [])),
                'disabled': input_field.has_attr('disabled'),
                'readonly': input_field.has_attr('readonly'),
                'attributes': {k: v for k, v in input_field.attrs.items() 
                              if k not in ['type', 'id', 'name', 'placeholder', 'value', 'required', 'class']}
            }
            inputs.append(input_info)
        
        # Find all textarea tags
        textarea_tags = soup.find_all('textarea')
        for textarea in textarea_tags:
            textarea_info = {
                'element_type': 'textarea',
                'id': textarea.get('id', ''),
                'name': textarea.get('name', ''),
                'placeholder': textarea.get('placeholder', ''),
                'value': textarea.text.strip(),
                'required': textarea.has_attr('required'),
                'class': ' '.join(textarea.get('class', [])),
                'disabled': textarea.has_attr('disabled'),
                'readonly': textarea.has_attr('readonly'),
                'rows': textarea.get('rows', ''),
                'cols': textarea.get('cols', ''),
                'attributes': {k: v for k, v in textarea.attrs.items() 
                              if k not in ['id', 'name', 'placeholder', 'required', 'class', 'rows', 'cols']}
            }
            inputs.append(textarea_info)
        
        # Find all select tags
        select_tags = soup.find_all('select')
        for select in select_tags:
            options = []
            for option in select.find_all('option'):
                options.append({
                    'value': option.get('value', ''),
                    'text': option.text.strip(),
                    'selected': option.has_attr('selected')
                })
            
            select_info = {
                'element_type': 'select',
                'id': select.get('id', ''),
                'name': select.get('name', ''),
                'required': select.has_attr('required'),
                'class': ' '.join(select.get('class', [])),
                'disabled': select.has_attr('disabled'),
                'multiple': select.has_attr('multiple'),
                'options': options,
                'attributes': {k: v for k, v in select.attrs.items() 
                              if k not in ['id', 'name', 'required', 'class', 'multiple']}
            }
            inputs.append(select_info)
        
        return inputs
    
    def _extract_forms(self, soup, driver):
        """Extract form elements from the page."""
        forms = []
        
        # Find all form tags
        form_tags = soup.find_all('form')
        for form in form_tags:
            # Extract form inputs
            form_inputs = []
            for input_field in form.find_all('input'):
                input_info = {
                    'type': input_field.get('type', 'text'),
                    'id': input_field.get('id', ''),
                    'name': input_field.get('name', ''),
                    'placeholder': input_field.get('placeholder', ''),
                    'value': input_field.get('value', ''),
                    'required': input_field.has_attr('required')
                }
                form_inputs.append(input_info)
            
            # Extract form submission elements
            submit_elements = []
            for submit in form.find_all(['button', 'input'], type=['submit', 'button']):
                submit_info = {
                    'element_type': 'submit_button' if submit.get('type') == 'submit' else 'button',
                    'text': submit.text.strip() if submit.name == 'button' else submit.get('value', ''),
                    'id': submit.get('id', ''),
                    'name': submit.get('name', '')
                }
                submit_elements.append(submit_info)
            
            form_info = {
                'element_type': 'form',
                'id': form.get('id', ''),
                'name': form.get('name', ''),
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'class': ' '.join(form.get('class', [])),
                'inputs': form_inputs,
                'submission_elements': submit_elements,
                'attributes': {k: v for k, v in form.attrs.items() 
                              if k not in ['id', 'name', 'action', 'method', 'class']}
            }
            forms.append(form_info)
        
        return forms
    
    def _get_page_structure(self, soup):
        """Extract basic page structure information."""
        structure = {
            'headers': [],
            'sections': [],
            'navigation': []
        }
        
        # Extract headers
        for header_tag in ['h1', 'h2', 'h3']:
            for header in soup.find_all(header_tag):
                structure['headers'].append({
                    'level': header_tag,
                    'text': header.text.strip(),
                    'id': header.get('id', '')
                })
        
        # Extract sections
        for section in soup.find_all(['div', 'section']):
            if section.get('id') or section.get('class'):
                structure['sections'].append({
                    'id': section.get('id', ''),
                    'class': ' '.join(section.get('class', []))
                })
        
        # Extract navigation
        nav_elements = soup.find_all(['nav', 'ul'])
        for nav in nav_elements:
            if nav.name == 'nav' or ('class' in nav.attrs and any('nav' in c.lower() for c in nav.get('class', []))):
                nav_items = []
                for link in nav.find_all('a'):
                    nav_items.append({
                        'text': link.text.strip(),
                        'href': link.get('href', '')
                    })
                if nav_items:
                    structure['navigation'].append({
                        'id': nav.get('id', ''),
                        'class': ' '.join(nav.get('class', [])),
                        'items': nav_items
                    })
        
        return structure
    
    def save_elements(self, elements, output_path):
        """
        Save the extracted elements to a JSON file.
        
        Args:
            elements (dict): The extracted elements.
            output_path (str): Path to save the elements JSON file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(elements, f, indent=2)

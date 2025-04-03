#!/usr/bin/env python3
"""
Test Case Generator module for generating test cases using GenAI.
This module handles Task 2 of the project: generating test cases based on extracted UI elements.
"""

import json
import os
import pandas as pd
from src.utils import load_template, get_user_input

class TestCaseGenerator:
    """Class responsible for generating test cases using AI."""
    
    def __init__(self, elements_json_path):
        """
        Initialize the TestCaseGenerator.
        
        Args:
            elements_json_path (str): Path to the JSON file containing extracted elements.
        """
        self.elements_json_path = elements_json_path
        self.elements = self._load_elements()
        self.test_cases = []
        
    def _load_elements(self):
        """
        Load element data from the JSON file.
        
        Returns:
            dict: The loaded elements data
            
        Raises:
            FileNotFoundError: If the elements JSON file does not exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(self.elements_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Elements file not found at: {self.elements_json_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.elements_json_path}")
    
    def generate_test_cases(self):
        """
        Generate test cases based on the extracted elements.
        This method:
        1. Creates an AI prompt based on the extracted elements
        2. Gets a response from the AI (either via API or manual entry)
        3. Processes the response into structured test cases
        
        Returns:
            list: The generated test cases
        """
        # Check if elements were loaded successfully
        if not self.elements:
            raise ValueError("No elements data available. Please check the elements JSON file.")
            
        # Load the prompt template
        try:
            prompt_template = load_template('templates/ai_prompts/test_case_prompt_template.txt')
        except FileNotFoundError:
            raise FileNotFoundError("Test case prompt template not found. Please check the templates directory.")
        
        # Create a formatted elements summary for the prompt
        elements_summary = self._format_elements_for_prompt()
        
        # Prepare the full prompt
        try:
            site_name = self.elements['metadata']['title']
            site_url = self.elements['metadata']['url']
        except KeyError:
            # Use placeholders if metadata is missing
            site_name = "Unknown Website"
            site_url = "Unknown URL"
            print("Warning: Website metadata missing from elements file.")
            
        prompt = prompt_template.format(
            site_name=site_name,
            site_url=site_url,
            elements_summary=elements_summary
        )
        
        print("\n" + "="*80)
        print("STEP 2: GENERATING TEST CASES")
        print("="*80)
        print("\nPlease provide the following prompt to your preferred GenAI tool (GPT-4, Claude, etc.):")
        print("\n" + "-"*40 + " PROMPT START " + "-"*40)
        print(prompt)
        print("-"*40 + " PROMPT END " + "-"*41 + "\n")
        
        # Get AI response (via manual input)
        ai_response = get_user_input("Paste the AI's response here (press Enter twice to finish):\n")
        
        # Process the response into structured test cases
        self._process_ai_response(ai_response)
        
        if not self.test_cases:
            print("\nWarning: No test cases were extracted from the AI response.")
            print("Please check the AI response format or modify the processing logic.")
        else:
            print(f"\nSuccessfully generated {len(self.test_cases)} test cases.")
            
        return self.test_cases
    
    def _format_elements_for_prompt(self):
        """
        Format the elements in a way suitable for the AI prompt.
        
        Returns:
            str: Formatted elements summary for the prompt
        """
        formatted_elements = []
        
        # Add site metadata if available
        if 'metadata' in self.elements and 'description' in self.elements['metadata']:
            formatted_elements.append(f"SITE DESCRIPTION: {self.elements['metadata']['description']}\n")
        
        # Format buttons
        if 'buttons' in self.elements and self.elements['buttons']:
            formatted_elements.append("BUTTONS:")
            for idx, button in enumerate(self.elements['buttons'], 1):
                text = button.get('text', '[No text]')
                element_type = button.get('element_type', 'button')
                element_id = button.get('id', '[No ID]')
                css_class = button.get('class', '[No class]')
                formatted_elements.append(f"  {idx}. {text} ({element_type}, id={element_id}, class={css_class})")
        
        # Format links
        if 'links' in self.elements and self.elements['links']:
            formatted_elements.append("\nLINKS:")
            for idx, link in enumerate(self.elements['links'], 1):
                text = link.get('text', '[No text]')
                href = link.get('href', '[No href]')
                target = link.get('target', '_self')
                formatted_elements.append(f"  {idx}. {text} (href={href}, target={target})")
        
        # Format input fields
        if 'inputs' in self.elements and self.elements['inputs']:
            formatted_elements.append("\nINPUT FIELDS:")
            for idx, input_field in enumerate(self.elements['inputs'], 1):
                input_type = input_field.get('element_type', 'input')
                
                if input_type == 'input':
                    field_type = input_field.get('type', 'text')
                    name = input_field.get('name', '[No name]')
                    placeholder = input_field.get('placeholder', '[No placeholder]')
                    required = 'required' if input_field.get('required', False) else 'optional'
                    formatted_elements.append(f"  {idx}. {field_type} input (name={name}, placeholder={placeholder}, {required})")
                
                elif input_type == 'textarea':
                    name = input_field.get('name', '[No name]')
                    placeholder = input_field.get('placeholder', '[No placeholder]')
                    rows = input_field.get('rows', 'default')
                    formatted_elements.append(f"  {idx}. textarea (name={name}, placeholder={placeholder}, rows={rows})")
                
                elif input_type == 'select':
                    name = input_field.get('name', '[No name]')
                    options = input_field.get('options', [])
                    options_count = len(options)
                    options_text = ", ".join([opt.get('text', 'Option') for opt in options[:5]])
                    if options_count > 5:
                        options_text += f", ... ({options_count-5} more)"
                    formatted_elements.append(f"  {idx}. select dropdown (name={name}, options: {options_text})")
        
        # Format forms
        if 'forms' in self.elements and self.elements['forms']:
            formatted_elements.append("\nFORMS:")
            for idx, form in enumerate(self.elements['forms'], 1):
                form_id = form.get('id', '[No ID]')
                method = form.get('method', 'get')
                action = form.get('action', '[No action]')
                inputs_count = len(form.get('inputs', []))
                formatted_elements.append(f"  {idx}. form (id={form_id}, method={method}, action={action}, {inputs_count} inputs)")
                
                # Add details about form inputs
                if form.get('inputs'):
                    for i, input_field in enumerate(form['inputs'], 1):
                        input_type = input_field.get('element_type', 'input')
                        field_type = input_field.get('type', 'text') if input_type == 'input' else input_type
                        name = input_field.get('name', '[No name]')
                        formatted_elements.append(f"    {i}. {field_type} (name={name})")
        
        # Add page structure info
        if 'metadata' in self.elements and 'page_structure' in self.elements['metadata']:
            page_structure = self.elements['metadata']['page_structure']
            
            if 'headers' in page_structure and page_structure['headers']:
                formatted_elements.append("\nPAGE HEADERS:")
                for header in page_structure['headers']:
                    level = header.get('level', 'h')
                    text = header.get('text', '[No text]')
                    formatted_elements.append(f"  - {level}: {text}")
            
            if 'navigation' in page_structure and page_structure['navigation']:
                formatted_elements.append("\nNAVIGATION MENUS:")
                for nav in page_structure['navigation']:
                    nav_id = nav.get('id', '[No ID]')
                    items = nav.get('items', [])
                    items_count = len(items)
                    formatted_elements.append(f"  - Navigation (id={nav_id}, {items_count} items)")
                    
                    # Add details about nav items
                    for i, item in enumerate(items[:5], 1):
                        text = item.get('text', '[No text]')
                        href = item.get('href', '[No href]')
                        formatted_elements.append(f"    {i}. {text} (href={href})")
                    if items_count > 5:
                        formatted_elements.append(f"    ... ({items_count-5} more items)")
        
        return "\n".join(formatted_elements)
    
    def _process_ai_response(self, response):
        """
        Process the AI response into structured test cases.
        
        Args:
            response (str): The AI response text
            
        Returns:
            list: The processed test cases
        """
        if not response.strip():
            print("Warning: Empty AI response received.")
            return []
            
        # Split response into lines
        lines = response.strip().split('\n')
        
        current_test_case = None
        section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for test case headers (Test Case ID markers)
            if (line.startswith('Test Case') and ':' in line) or (line.startswith('TC-') and ':' in line):
                # Save previous test case if it exists
                if current_test_case:
                    self.test_cases.append(current_test_case)
                
                # Start a new test case
                parts = line.split(':', 1)
                test_id = parts[0].strip()
                test_scenario = parts[1].strip() if len(parts) > 1 else ""
                current_test_case = {
                    'Test Case ID': test_id,
                    'Test Scenario': test_scenario,
                    'Steps to Execute': [],
                    'Expected Result': ''
                }
                section = None
            
            # Look for section headers
            elif line.lower().startswith('steps to execute') or line.lower() == 'steps':
                section = 'Steps to Execute'
            elif line.lower().startswith('expected result') or line.lower() == 'expected':
                section = 'Expected Result'
                
            # Add content to current section
            elif section and current_test_case:
                if section == 'Steps to Execute':
                    # Check if this is a numbered step
                    if line[0].isdigit() and '. ' in line:
                        step_number = line.split('. ')[0]
                        step_text = line[len(step_number) + 2:].strip()
                        current_test_case[section].append(step_text)
                    else:
                        # Continuation of previous step or unnumbered step
                        if current_test_case[section]:
                            # Check if it's just a continuation
                            if not line[0].isdigit() or '. ' not in line:
                                current_test_case[section][-1] += " " + line
                            else:
                                # It's a new step without proper numbering
                                current_test_case[section].append(line)
                        else:
                            current_test_case[section].append(line)
                else:  # Expected Result section
                    if current_test_case[section]:
                        current_test_case[section] += " " + line
                    else:
                        current_test_case[section] = line
        
        # Don't forget to add the last test case
        if current_test_case:
            self.test_cases.append(current_test_case)
            
        return self.test_cases
    
    def save_test_cases(self, output_path):
        """
        Save the generated test cases to an Excel file.
        
        Args:
            output_path (str): Path to save the test cases Excel file.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.test_cases:
            print("Error: No test cases to save.")
            return False
            
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Convert the steps list to a string for Excel
            processed_test_cases = []
            for test_case in self.test_cases:
                processed_case = test_case.copy()
                
                if isinstance(processed_case['Steps to Execute'], list):
                    # Convert list of steps to numbered steps
                    steps_text = ""
                    for i, step in enumerate(processed_case['Steps to Execute'], 1):
                        steps_text += f"{i}. {step}\n"
                    processed_case['Steps to Execute'] = steps_text.strip()
                    
                processed_test_cases.append(processed_case)
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(processed_test_cases)
            df.to_excel(output_path, index=False)
            print(f"\nTest cases successfully saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving test cases to Excel: {str(e)}")
            return False
            
    def get_test_cases(self):
        """
        Get the current test cases.
        
        Returns:
            list: The current test cases
        """
        return self.test_cases
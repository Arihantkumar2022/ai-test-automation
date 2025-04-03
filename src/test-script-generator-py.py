#!/usr/bin/env python3
"""
Test Script Generator module for creating Selenium test scripts.
This module handles Task 3 of the project: generating Selenium scripts for test cases.
"""

import pandas as pd
from src.utils import load_template, get_user_input

class TestScriptGenerator:
    """Class responsible for generating Selenium test scripts using AI."""
    
    def __init__(self, test_cases_path):
        """
        Initialize the TestScriptGenerator.
        
        Args:
            test_cases_path (str): Path to the Excel file containing test cases.
        """
        self.test_cases_path = test_cases_path
        self.test_cases = self._load_test_cases()
        self.test_scripts = []
        
    def _load_test_cases(self):
        """Load test cases from the Excel file."""
        return pd.read_excel(self.test_cases_path).to_dict('records')
    
    def generate_scripts(self):
        """
        Generate Selenium scripts for each test case.
        This method:
        1. For each test case, creates an AI prompt
        2. Gets a response from the AI (either via API or manual entry)
        3. Processes the response into structured test scripts
        """
        # Load the prompt template
        prompt_template = load_template('ai_prompts/test_script_prompt_template.txt')
        
        print("\n" + "="*80)
        print("STEP 2: GENERATING SELENIUM SCRIPTS")
        print("="*80)
        
        for i, test_case in enumerate(self.test_cases, 1):
            test_id = test_case['Test Case ID']
            test_scenario = test_case['Test Scenario']
            steps = test_case['Steps to Execute']
            expected_result = test_case['Expected Result']
            
            # Prepare the full prompt
            prompt = prompt_template.format(
                test_id=test_id,
                test_scenario=test_scenario,
                steps=steps,
                expected_result=expected_result
            )
            
            print(f"\nGenerating script for {test_id}: {test_scenario} ({i}/{len(self.test_cases)})")
            print("\n" + "-"*40 + " PROMPT START " + "-"*40)
            print(prompt)
            print("-"*40 + " PROMPT END " + "-"*41 + "\n")
            
            # Get AI response (via manual input)
            ai_response = get_user_input(f"Paste the AI's response for {test_id} (press Enter twice to finish):\n")
            
            # Extract the code from the AI response
            script_code = self._extract_code_from_response(ai_response)
            
            # Store the generated script
            self.test_scripts.append({
                'Test Case ID': test_id,
                'Test Scenario': test_scenario,
                'Python Selenium Code': script_code
            })
            
            print(f"Script for {test_id} generated successfully.")
        
        print(f"\nAll {len(self.test_scripts)} scripts generated successfully.")
    
    def _extract_code_from_response(self, response):
        """
        Extract the Python code from the AI response.
        Assumes the code is enclosed in markdown code blocks (```python ... ```).
        """
        lines = response.strip().split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith("```python") or line.strip() == "```python":
                in_code_block = True
                continue
            elif line.strip() == "```" and in_code_block:
                in_code_block = False
                continue
            
            if in_code_block:
                code_lines.append(line)
            
        # If no code blocks found, try to extract raw Python code
        if not code_lines:
            # Look for import statements as markers of Python code
            in_code = False
            for line in lines:
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    in_code = True
                
                if in_code:
                    code_lines.append(line)
        
        # If still no code found, assume the entire response is code
        if not code_lines:
            code_lines = lines
            
        return "\n".join(code_lines)
    
    def save_scripts(self, output_path):
        """
        Save the generated scripts to an Excel file.
        
        Args:
            output_path (str): Path to save the scripts Excel file.
        """
        df = pd.DataFrame(self.test_scripts)
        df.to_excel(output_path, index=False)

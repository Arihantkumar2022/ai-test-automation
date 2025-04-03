#!/usr/bin/env python3
"""
Main entry point for the AI-driven test automation prototype.
This script orchestrates the entire process of web scraping, test case generation,
and test script generation.
"""

import os
import argparse
from src.element_extractor import ElementExtractor
from src.test_case_generator import TestCaseGenerator
from src.test_script_generator import TestScriptGenerator
from src.utils import setup_directories, validate_url

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AI-Driven Test Automation Prototype')
    parser.add_argument('--url', type=str, help='Target website URL')
    parser.add_argument(
        '--task', 
        type=str, 
        choices=['extract', 'generate_tests', 'generate_scripts', 'all'],
        default='all',
        help='Specific task to run'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='./output',
        help='Output directory for generated files'
    )
    parser.add_argument(
        '--ai-provider', 
        type=str, 
        choices=['openai', 'anthropic', 'perplexity'],
        default='manual',
        help='AI provider to use (currently only manual mode is supported)'
    )
    
    return parser.parse_args()

def main():
    """Main function to orchestrate the automation workflow."""
    args = parse_arguments()
    
    # Setup directories
    setup_directories(args.output)
    
    # Define file paths
    elements_json_path = os.path.join(args.output, 'elements.json')
    test_cases_path = os.path.join(args.output, 'test_cases.xlsx')
    test_scripts_path = os.path.join(args.output, 'test_scripts.xlsx')
    
    # Execute tasks based on user selection
    if args.task in ['extract', 'all']:
        if not args.url:
            raise ValueError("URL is required for extraction task. Use --url parameter.")
        
        print(f"Task 1: Extracting elements from {args.url}")
        if not validate_url(args.url):
            raise ValueError(f"Invalid URL: {args.url}")
            
        extractor = ElementExtractor(args.url)
        elements = extractor.extract_elements()
        extractor.save_elements(elements, elements_json_path)
        print(f"Elements saved to {elements_json_path}")
    
    if args.task in ['generate_tests', 'all']:
        print("Task 2: Generating test cases using AI")
        if not os.path.exists(elements_json_path):
            raise FileNotFoundError(f"Elements file not found: {elements_json_path}. Run extraction task first.")
            
        test_generator = TestCaseGenerator(elements_json_path)
        test_generator.generate_test_cases()
        test_generator.save_test_cases(test_cases_path)
        print(f"Test cases saved to {test_cases_path}")
    
    if args.task in ['generate_scripts', 'all']:
        print("Task 3: Generating Selenium scripts using AI")
        if not os.path.exists(test_cases_path):
            raise FileNotFoundError(f"Test cases file not found: {test_cases_path}. Run test case generation task first.")
            
        script_generator = TestScriptGenerator(test_cases_path)
        script_generator.generate_scripts()
        script_generator.save_scripts(test_scripts_path)
        print(f"Test scripts saved to {test_scripts_path}")
    
    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()

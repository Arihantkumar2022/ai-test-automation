# AI-Driven Test Automation Prototype

A Python-based prototype that uses AI to automatically generate test cases and Selenium scripts from website elements. This project consists of three main components:

1. **Web Scraping & UI Element Extraction**: Extract UI elements from a website
2. **Test Case Generation**: Generate test cases using AI based on extracted elements
3. **Selenium Script Generation**: Create Selenium scripts for automated testing

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Challenges and Solutions](#challenges-and-solutions)
- [Future Improvements](#future-improvements)
- [GenAI Conversation Link](#genai-conversation-link)

## Project Overview

This project aims to simplify test automation by using AI to generate test cases and scripts. The workflow is as follows:

1. **Task 1**: The application scrapes a given website to extract UI elements (buttons, links, forms, input fields).
2. **Task 2**: The extracted elements are analyzed using GenAI to generate meaningful test cases.
3. **Task 3**: For each test case, the system generates corresponding Selenium test scripts.

## Installation

### Prerequisites
- Python 3.8 or higher
- Access to a GenAI model (such as GPT-4, Claude, or Perplexity)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Arihantkumar2022/ai-test-automation.git
   cd ai-test-automation
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Entire Process

To run the entire process (web scraping, test case generation, and script generation), use:

```bash
python main.py --url https://demoblaze.com
```

### Running Individual Tasks

For individual tasks:

1. **Task 1 - Web Scraping**:
   ```bash
   python main.py --task extract --url https://demoblaze.com
   ```

2. **Task 2 - Test Case Generation**:
   ```bash
   python main.py --task generate_tests
   ```

3. **Task 3 - Script Generation**:
   ```bash
   python main.py --task generate_scripts
   ```

### Command-line Arguments

- `--url`: Target website URL (required for Task 1)
- `--task`: Specific task to run (`extract`, `generate_tests`, `generate_scripts`, or `all`)
- `--output`: Custom output directory (default: `./output`)
- `--ai-provider`: AI provider to use (`openai`, `anthropic`, `perplexity`) - Note: for this prototype, AI prompts are manual

## Project Structure

- `src/element_extractor.py`: Handles web scraping and element extraction
- `src/test_case_generator.py`: Manages test case generation using AI
- `src/test_script_generator.py`: Manages Selenium script generation using AI
- `src/utils.py`: Contains utility functions for the project
- `templates/`: Contains templates for AI prompts and output files
- `output/`: Default directory for generated files

## Implementation Details

### Task 1: Web Scraping & UI Element Extraction

The element extraction process uses Selenium and BeautifulSoup to:
1. Load and render the target website
2. Identify key UI elements (buttons, links, forms, input fields)
3. Extract relevant attributes (ID, name, text, type, etc.)
4. Structure the data into a JSON format
5. Save the extracted elements to `elements.json`

The extractor captures the following information:
- Element type
- Element attributes (ID, class, name)
- Element text content
- Element location on the page
- Parent-child relationships

### Task 2: Test Case Generation

The test case generation process:
1. Loads the extracted elements from `elements.json`
2. Uses a carefully crafted prompt template to instruct the AI
3. Sends the prompt to the GenAI model
4. Processes the AI's response into structured test cases
5. Exports the test cases to `test_cases.xlsx` with the following fields:
   - Test Case ID
   - Test Scenario
   - Steps to Execute
   - Expected Result

### Task 3: Selenium Script Generation

The script generation process:
1. Loads the test cases from `test_cases.xlsx`
2. For each test case, creates a specialized prompt for the AI
3. Sends the prompt to the GenAI model to generate Selenium code
4. Validates and formats the generated code
5. Exports the scripts to `test_scripts.xlsx`

## Challenges and Solutions

### Challenge 1: Dynamic Website Content
**Solution**: Used Selenium with sufficient wait times to ensure dynamic content loads before extraction.

### Challenge 2: AI Prompt Engineering
**Solution**: Created detailed prompt templates with explicit instructions about format and context to generate consistent and useful output.

### Challenge 3: Converting AI Output to Structured Data
**Solution**: Implemented robust parsing logic to extract structured data from AI responses.

### Challenge 4: Handling Different Website Structures
**Solution**: Created a flexible element extraction approach that adapts to various website layouts.

## Future Improvements

1. **API Integration**: Direct integration with AI provider APIs instead of manual prompting
2. **Enhanced Element Analysis**: More sophisticated element relationship analysis
3. **Test Execution**: Adding functionality to execute generated scripts
4. **Improved UI Element Classification**: Better identification of UI components based on functionality
5. **Feedback Loop**: Incorporate test execution results to improve future test generation
6. **Support for More Complex Scenarios**: Handle multi-page flows and state-dependent interactions



---

This README provides an overview of the project implementation, usage instructions, and potential improvements. For any questions or issues, please reach out.

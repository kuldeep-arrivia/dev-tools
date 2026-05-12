import os

import requests
import json
import re
from pathlib import Path


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b")
PROMPT_FILE = "categorization-criteria-prompt.txt"

def load_prompt_template():

    current_dir = Path(__file__).parent

    prompt_path = current_dir / PROMPT_FILE

    print(f"Looking for prompt file at: {prompt_path}")

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

PROMPT = load_prompt_template()

def get_category_and_reason(test_case):

    print("started calculating category using LLM for test case :")
    print(test_case)


    try:

        # Read prompt template from file
        prompt_template = PROMPT

        # Inject dynamic content
        prompt = prompt_template.format(steps=test_case)

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        result = response.json()

        raw_output = result.get("response", "").strip()

        # Extract JSON block
        match = re.search(
            r"\{.*\}",
            raw_output,
            re.DOTALL
        )

        if match:

            json_str = match.group(0)

            try:
                parsed_output = json.loads(json_str)

            except json.JSONDecodeError:
                parsed_output = {}

        else:
            parsed_output = {}

       

        category = normalize_category(
            parsed_output.get("category", "")
        )

        reason = parsed_output.get("reason", "")
        print("---- result ---")
        print(
            f"category: {category}, reason: {reason}"
        )
        
        print("Finished calculating category using LLM")
        print("==============================================")

        return {
            "category": category,
            "reason": reason
        }

    except requests.exceptions.RequestException as e:

        return {
            "category": "none",
            "reason": str(e)
        }

    except Exception as e:

        return {
            "category": "none",
            "error": f"Unexpected error: {str(e)}"
        }
    
def normalize_category(output):
    """
    Ensures output maps to one of the valid categories.
    """
    output = output.lower()

    if "critical" in output:
        return "Critical"
    elif "high" in output:
        return "High"
    elif "medium" in output:
        return "Medium"
    else:
        return "Low"


# Example usage
if __name__ == "__main__":
    test_case = {
        "id": "123848",
        "steps": """
                1. Given an Agent is on the Member Search
                2. When adding the Member ID
                3. And clicking the Search button 
                4. Then the correct results will appear at the bottom of the page under the Search button 

        """
    }

    #result = get_category_and_reason(test_case)#

    #print(json.dumps(result, indent=2))
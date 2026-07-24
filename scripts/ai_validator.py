import os
import sys
from google import genai
from google.genai import types

def get_directory_structure(root_dir="."):
    """Generates a text-based tree representation of the repository."""
    structure = []
    # Ignore virtual environments, git data, and local cache layers
    ignored_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.aws-sam'}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{sub_indent}{f}")
            
    return "\n".join(structure)

def validate_structure():
    # Automatically picks up the GEMINI_API_KEY environment variable
    client = genai.Client()
    repo_layout = get_directory_structure()
    
    prompt = f"""
    You are an AWS Serverless (SAM) and CI/CD DevOps expert. 
    Analyze this project's directory structure for a GitHub Actions deployment workflow:
    
    {repo_layout}
    
    This is an AWS SAM project. Verify if the structure looks correct for a standard deployment. 
    Look for missing critical configurations like:
    - A root level 'template.yaml' or 'template.yml' (Required for SAM applications).
    - Code source directories matching handlers (like the 'src' directory).
    - Necessary configuration files like 'requirements-dev.txt' or 'samconfig.toml'.
    
    Your response must strictly follow this format:
    STATUS: [PASSED or FAILED]
    REASON: [Brief explanation of what is missing or incorrect, or 'All structures verified' if passed]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        result_text = response.text
        print("--- AI Validation Output ---")
        print(result_text)
        print("----------------------------")
        
        if "STATUS: FAILED" in result_text:
            print("❌ AI Validation Failed. Stopping the workflow.")
            sys.exit(1)
        else:
            print("✅ AI Validation Passed. Proceeding with workflow.")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Error communicating with Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_structure()

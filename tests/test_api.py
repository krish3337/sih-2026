import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Import config, which calls load_dotenv()
from ai_core.config import create_llm_client

def main():
    print("Checking environment...")
    
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
        
    print("✓ .env loaded successfully.")
    print("✓ GEMINI_API_KEY is present in the environment (value hidden).")
    
    try:
        llm = create_llm_client()
    except Exception as e:
        print(f"Failed to instantiate GeminiClient: {e}")
        sys.exit(1)
        
    print("Making minimal test call to Gemini API...")
    try:
        response = llm.generate("Respond with only the word 'SUCCESS'.")
        print(f"✓ API Call Succeeded. Model responded with: {response}")
    except Exception as e:
        print(f"✗ API Call Failed. Exact Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()

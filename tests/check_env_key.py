import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY", "")
    
    if not key:
        print("GEMINI_API_KEY is completely empty or not loaded.")
        return

    print("--- KEY DIAGNOSTICS ---")
    print(f"Length: {len(key)}")
    print(f"Repr:   {repr(key)}")
    
    if key.startswith("AQ."):
        print("Prefix: Starts with 'AQ.'")
    elif key.startswith("AIzaSy"):
        print("Prefix: Starts with 'AIzaSy'")
    else:
        print("Prefix: Unknown format")
        
    has_whitespace = any(c.isspace() for c in key)
    print(f"Contains any whitespace: {has_whitespace}")

if __name__ == "__main__":
    main()

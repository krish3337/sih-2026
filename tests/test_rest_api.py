import os
import sys
import urllib.request
import urllib.error
from dotenv import load_dotenv

def main():
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not found.")
        sys.exit(1)

    # Standard Gemini API models endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            
            # Sanitize just in case
            sanitized_body = body.replace(key, "[REDACTED_API_KEY]")
            
            print(f"HTTP Status: {status}")
            print(f"Response: {sanitized_body}")
            
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        
        # Sanitize just in case
        sanitized_body = body.replace(key, "[REDACTED_API_KEY]")
        
        print(f"HTTP Status: {status}")
        print(f"Response Error: {sanitized_body}")
        
    except Exception as e:
        print(f"Unknown Error: {e}")

if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        print("Making generate_content call using google-genai Client...")
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Say 'SUCCESS' if you receive this."
        )
        print(f"\nResponse: {response.text}")
    except Exception as e:
        print(f"\nExact Error: {e}")

if __name__ == "__main__":
    main()

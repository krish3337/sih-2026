import os
import sys

def main():
    dirs = ["ai_core", "scripts", "tests"]
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    new_content = content.replace("from src.", "from ai_core.")
                    new_content = new_content.replace("from src ", "from ai_core ")
                    new_content = new_content.replace("import src.", "import ai_core.")
                    new_content = new_content.replace("import src\n", "import ai_core\n")
                    
                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as file:
                            file.write(new_content)
                        print(f"Updated {path}")

if __name__ == "__main__":
    main()

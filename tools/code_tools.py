import os
from crewai.tools import tool

@tool("Reads Python source code files from directory")
def read_code_files(directory="code_snippet", extensions=(".py",), max_files=5):
    """Reads Python source code files from a specified directory and returns their contents."""
    code_snippets = []
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    code_snippets.append((file, content))
                count += 1
            if count >= max_files:
                break
    return code_snippets

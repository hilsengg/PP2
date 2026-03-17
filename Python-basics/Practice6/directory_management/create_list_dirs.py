import os
from pathlib import Path

os.makedirs("parent/child/grandchild", exist_ok=True)

print("Current Directory Contents:", os.listdir("."))


py_files = [f for f in os.listdir(".") if f.endswith(".py")]
print(f"Python files found: {py_files}")
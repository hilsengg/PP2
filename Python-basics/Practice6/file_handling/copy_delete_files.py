import shutil
import os

shutil.copy("sample.txt", "sample_backup.txt")

if os.path.exists("sample.txt"):
    os.remove("sample.txt")
    print("Original file deleted.")
from pathlib import Path
import shutil

Path("data.txt").touch()
Path("archive").mkdir(exist_ok=True)

shutil.move("data.txt", "archive/data_v1.txt")
with open("sample.txt", "r") as f:
    content = f.readlines()
    for line in content:
        print(f"Line: {line.strip()}")
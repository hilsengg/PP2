names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for index, name in enumerate(names):
    print(f"{index}: {name}")

for name, score in zip(names, scores):
    print(f"{name} scored {score}")
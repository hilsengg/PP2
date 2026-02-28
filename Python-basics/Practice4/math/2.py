#Write a Python program to calculate the area of a trapezoid.
"""
Height: 5
Base, first value: 5
Base, second value: 6
Expected Output: 27.5
"""
h = int(input())
b1 = int(input())
b2 = int(input())

print("Height:", h)
print("Base, first value:", b1)
print("Base, second value:", b2)
A = ((b1+b2)/2)*h
print("Expected Output:", A)
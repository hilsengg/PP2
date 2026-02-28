#Write a Python program to calculate the area of regular polygon.
"""
Input number of sides: 4
Input the length of a side: 25
The area of the polygon is: 625
"""
import math
n = int(input("number of sides:"))
a = int(input("length of a side:"))
s = a*a*n*(1/4)*(math.tan((math.pi)*(n-2)/(2*n)))
print(round(s))
#Write a Python program to calculate two date difference in seconds.
from datetime import *
current = datetime(2022, 12, 11, 13, 24, 15)
second = datetime(2021, 10, 24, 13, 15, 21)
difference = current - second
total = difference.total_seconds()
print(total)
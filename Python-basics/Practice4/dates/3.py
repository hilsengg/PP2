#Write a Python program to drop microseconds from datetime.
import datetime
x = datetime.datetime.now()
m = x.replace(microsecond=0)
print(m)
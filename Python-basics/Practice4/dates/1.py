#Write a Python program to subtract five days from current date.
import datetime
x = datetime.datetime.now()

a = x - datetime.timedelta(days=5)  #day-5

print(a)
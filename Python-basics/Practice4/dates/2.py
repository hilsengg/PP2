#Write a Python program to print yesterday, today, tomorrow.
import datetime
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)
yesterday = today - datetime.timedelta(days=1)
print(yesterday)
print(today)
print(tomorrow)
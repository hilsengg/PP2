x = "fun"

def myfunc():
  x = "interesting"
  print("Python is " + x)

myfunc()

print("Python is " + x)

def my2func():
  global y
  y = "Fantastic"

my2func()
print("Python is", y)
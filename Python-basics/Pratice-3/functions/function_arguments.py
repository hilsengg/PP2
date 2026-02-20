def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")


def my_function1(a, b, /, *, c, d):
  return a + b + c + d

result = my_function1(5, 10, c = 15, d = 20)
print(result)
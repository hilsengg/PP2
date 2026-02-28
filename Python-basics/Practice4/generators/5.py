#Implement a generator that returns all numbers from (n) down to 0.
def returning(n):
    for i in range(n+1, -1, -1):
        yield i

ret = returning(9)
for i in range(11):
    print(next(ret))
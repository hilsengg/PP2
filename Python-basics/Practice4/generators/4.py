#Implement a generator called squares to yield the square of all numbers from (a) to (b). 
#Test it with a "for" loop and print each of the yielded values.
def squares_inrange(a, b):
    for i in range(a, b+1):
        yield (i*i)

squares = squares_inrange(2, 10)
for i in range(2, 11):
    print(next(squares))
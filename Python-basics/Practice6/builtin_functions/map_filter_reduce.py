from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x**2, nums))

evens = list(filter(lambda x: x % 2 == 0, nums))

total = reduce(lambda x, y: x + y, nums)

print(f"Squared: {squared}, Evens: {evens}, Total: {total}")
from time import perf_counter
import f


t1 = perf_counter()

for number in range(10000):
    str(f'the number is {number}')

print(perf_counter() - t1)

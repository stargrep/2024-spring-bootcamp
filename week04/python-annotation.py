# https://realpython.com/primer-on-python-decorators/
# https://www.geeksforgeeks.org/function-decorators-in-python-set-1-introduction/
import time
import functools


def timed(func):
    @functools.wraps(func)
    def wrapper_once(*args, **kwargs):
        print(f"{func} started")
        start_time = time.perf_counter()
        value = func(*args, **kwargs)  # func = foo
        end_time = time.perf_counter()
        print(f"Time is: {end_time - start_time}")
        return value

    return wrapper_once


@timed
def foo(n, m):
    res = 0
    for _ in range(n):
        res += sum([i ** 3 for i in range(m)])
    return res


print(foo(1000, 100))
print(foo.__name__)

# timed
# logging
# functools
# rate_limit
# routing
# login

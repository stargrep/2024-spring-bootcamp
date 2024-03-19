# 注意 - Copy this file and rename as assignment3_{first_name}.py then complete code with a pull request(PR).

# Q1. Given a positive integer N. The task is to write a Python program to check if the number is prime or not.
from typing import Tuple


def is_prime(n: int) -> bool:
    if n == 1:
        return False

    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1

    return True


# DO NOT ALTER BELOW.
assert is_prime(2)
assert not is_prime(15)
assert is_prime(17)
assert is_prime(29)
assert is_prime(7907)



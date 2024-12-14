# utils.py
import math

def is_power_of_two(n):
    """Checks if a number is a power of two."""
    return (n > 0) and (n & (n - 1) == 0)

def next_power_of_two(n):
    """Calculates the next power of two greater than or equal to n."""
    if is_power_of_two(n):
        return n
    return 2**(math.ceil(math.log2(n)))

def calculate_order(size):
    """Calculates the order of a block given its size (size must be a power of 2)."""
    if not is_power_of_two(size):
        raise ValueError("Size must be a power of 2")
    return int(math.log2(size))
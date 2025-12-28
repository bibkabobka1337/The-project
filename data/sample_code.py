"""
Sample Python code for testing the Code Quality Assessment Tool.

This file contains examples of code with various quality levels.
"""


def simple_function(x):
    """A simple function with good quality."""
    return x * 2


def complex_function(data):
    """A more complex function."""
    result = []
    if data:
        for item in data:
            if item > 0:
                if item % 2 == 0:
                    result.append(item * 2)
                else:
                    result.append(item)
    return result


class Calculator:
    """A simple calculator class."""

    def __init__(self):
        """Initialize the calculator."""
        self.history = []

    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result


def function_without_docstring(x):
    return x + 1


# Some duplicate code for testing duplication detection
def duplicate_block_1():
    x = 1
    y = 2
    z = 3
    return x + y + z


def duplicate_block_2():
    x = 1
    y = 2
    z = 3
    return x * y * z


"""
Clean, well-written code examples for training
"""

def calculate_factorial(number):
    """Calculate factorial of a positive integer."""
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if number == 0 or number == 1:
        return 1
    return number * calculate_factorial(number - 1)


def find_maximum(numbers):
    """Find the maximum value in a list of numbers."""
    if not numbers:
        raise ValueError("Cannot find maximum of empty list")
    return max(numbers)


def is_prime(number):
    """Check if a number is prime."""
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def fibonacci_sequence(count):
    """Generate fibonacci sequence up to count numbers."""
    if count <= 0:
        return []
    elif count == 1:
        return [0]
    elif count == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, count):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence


class Calculator:
    """Simple calculator with basic operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract second number from first."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a, b):
        """Divide first number by second."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class BankAccount:
    """Simple bank account implementation."""
    
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    
    def deposit(self, amount):
        """Deposit money to account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        """Withdraw money from account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_balance(self):
        """Get current balance."""
        return self.balance


def validate_email(email):
    """Simple email validation."""
    if '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    if not parts[0] or not parts[1]:
        return False
    return True


def sort_students_by_grade(students):
    """Sort list of student dictionaries by grade."""
    return sorted(students, key=lambda student: student.get('grade', 0))


def count_word_frequency(text):
    """Count frequency of words in text."""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency
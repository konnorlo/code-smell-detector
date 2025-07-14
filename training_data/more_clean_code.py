"""
Additional clean code examples for better training diversity
"""

class ShoppingCart:
    """Well-designed shopping cart implementation."""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, product, quantity=1):
        """Add item to cart."""
        self.items.append({'product': product, 'quantity': quantity})
    
    def remove_item(self, product):
        """Remove item from cart."""
        self.items = [item for item in self.items if item['product'] != product]
    
    def get_total(self):
        """Calculate total cart value."""
        return sum(item['product']['price'] * item['quantity'] for item in self.items)
    
    def is_empty(self):
        """Check if cart is empty."""
        return len(self.items) == 0


def binary_search(arr, target):
    """Perform binary search on sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def merge_sorted_arrays(arr1, arr2):
    """Merge two sorted arrays into one sorted array."""
    result = []
    i = j = 0
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


def calculate_statistics(numbers):
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        return None
    
    return {
        'mean': sum(numbers) / len(numbers),
        'median': sorted(numbers)[len(numbers) // 2],
        'min': min(numbers),
        'max': max(numbers),
        'count': len(numbers)
    }


class FileManager:
    """Simple file operations manager."""
    
    def read_file(self, filename):
        """Read file content."""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def write_file(self, filename, content):
        """Write content to file."""
        with open(filename, 'w') as f:
            f.write(content)
    
    def file_exists(self, filename):
        """Check if file exists."""
        import os
        return os.path.exists(filename)


def quicksort(arr):
    """Implement quicksort algorithm."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def parse_csv_line(line):
    """Parse a CSV line into fields."""
    fields = []
    current_field = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(current_field.strip())
            current_field = ""
        else:
            current_field += char
    
    fields.append(current_field.strip())
    return fields


class Queue:
    """Simple queue implementation using list."""
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Add item to rear of queue."""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)
    
    def is_empty(self):
        """Check if queue is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Get queue size."""
        return len(self.items)


def format_currency(amount, currency='USD'):
    """Format amount as currency string."""
    if currency == 'USD':
        return f"${amount:.2f}"
    elif currency == 'EUR':
        return f"€{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"


def validate_phone_number(phone):
    """Validate phone number format."""
    import re
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    return bool(re.match(pattern, phone))


class Stack:
    """Simple stack implementation."""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Push item onto stack."""
        self.items.append(item)
    
    def pop(self):
        """Pop item from stack."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Peek at top item without removing."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty."""
        return len(self.items) == 0
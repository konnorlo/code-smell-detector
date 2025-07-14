"""
Mixed quality code with some good and some bad patterns
"""

def calculate_area(length, width):
    """Good function - clear purpose and naming."""
    return length * width


def x(a, b):
    # Bad naming
    return a + b


class UserManager:
    """Well-designed class with reasonable methods."""
    
    def __init__(self):
        self.users = []
    
    def add_user(self, username, email):
        """Add a new user."""
        user = {'username': username, 'email': email}
        self.users.append(user)
    
    def remove_user(self, username):
        """Remove user by username."""
        self.users = [u for u in self.users if u['username'] != username]
    
    def find_user(self, username):
        """Find user by username."""
        for user in self.users:
            if user['username'] == username:
                return user
        return None
    
    def temp_method(self):
        # Poor naming
        return len(self.users)


def process_order_and_calculate_shipping_and_tax_and_validate_inventory():
    # Long method name indicates it does too much
    order_total = 0
    tax_rate = 0.08
    shipping_cost = 10
    
    items = [
        {'name': 'item1', 'price': 25, 'quantity': 2},
        {'name': 'item2', 'price': 15, 'quantity': 1},
        {'name': 'item3', 'price': 30, 'quantity': 3}
    ]
    
    # Calculate total
    for item in items:
        order_total += item['price'] * item['quantity']
    
    # Add tax
    tax_amount = order_total * tax_rate
    order_total += tax_amount
    
    # Add shipping
    if order_total < 50:
        order_total += shipping_cost
    
    # Validate inventory (should be separate function)
    for item in items:
        if item['quantity'] > 10:
            return False, "Insufficient inventory"
    
    return True, order_total


def validate_password(password):
    """Good function with clear validation logic."""
    if len(password) < 8:
        return False, "Password too short"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and digits"
    
    return True, "Password valid"


def foo_bar_baz(x, y, z, a, b, c, d, e, f, g):
    # Poor naming and too many parameters
    if x and y and z and a and b and c and d and e and f and g:
        return True
    return False


class DataProcessor:
    """Reasonably well-designed class."""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.processed_data = []
    
    def load_data(self):
        """Load data from source."""
        # Simulated data loading
        self.data = [1, 2, 3, 4, 5]
    
    def process_data(self):
        """Process the loaded data."""
        self.processed_data = [x * 2 for x in self.data]
    
    def get_results(self):
        """Get processed results."""
        return self.processed_data


def complex_condition_example(user, order, inventory):
    if user and user.get('active') and user.get('verified') and order and order.get('total') > 0 and order.get('items') and inventory and inventory.get('available') and len(order.get('items', [])) > 0:
        return True
    return False


def simple_function():
    """This is a well-written simple function."""
    return "Hello, World!"


def another_long_function_that_does_too_many_things():
    # This function violates single responsibility
    data = []
    
    # Data collection
    for i in range(50):
        data.append(i)
    
    # Data filtering
    filtered_data = []
    for item in data:
        if item % 2 == 0:
            filtered_data.append(item)
    
    # Data transformation
    transformed_data = []
    for item in filtered_data:
        transformed_data.append(item * 3)
    
    # Data aggregation
    total = sum(transformed_data)
    average = total / len(transformed_data)
    
    # Result formatting
    result = {
        'data': transformed_data,
        'total': total,
        'average': average,
        'count': len(transformed_data)
    }
    
    return result
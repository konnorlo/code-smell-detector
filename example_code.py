import os
import sys
from typing import List, Dict, Any


def x():
    pass


def foo():
    return True


def extremely_long_method_that_should_be_detected_as_a_smell():
    """This method is intentionally long to trigger the long method smell"""
    variable_one = 1
    variable_two = 2
    variable_three = 3
    variable_four = 4
    variable_five = 5
    variable_six = 6
    variable_seven = 7
    variable_eight = 8
    variable_nine = 9
    variable_ten = 10
    variable_eleven = 11
    variable_twelve = 12
    variable_thirteen = 13
    variable_fourteen = 14
    variable_fifteen = 15
    variable_sixteen = 16
    variable_seventeen = 17
    variable_eighteen = 18
    variable_nineteen = 19
    variable_twenty = 20
    variable_twenty_one = 21
    variable_twenty_two = 22
    variable_twenty_three = 23
    variable_twenty_four = 24
    variable_twenty_five = 25
    variable_twenty_six = 26
    variable_twenty_seven = 27
    variable_twenty_eight = 28
    variable_twenty_nine = 29
    variable_thirty = 30
    variable_thirty_one = 31
    variable_thirty_two = 32
    variable_thirty_three = 33
    variable_thirty_four = 34
    variable_thirty_five = 35
    return variable_thirty_five


def complex_conditional_method(x, y, z, a, b, c, d, e):
    if x > 0 and y < 10 and z == 5 and a != b and c in [1, 2, 3] and d not in [4, 5, 6] and e > 100:
        return True
    return False


def high_complexity_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                for j in range(i):
                    if j > 5:
                        while j > 0:
                            if j % 3 == 0:
                                try:
                                    if j > 10:
                                        for k in range(j):
                                            if k % 4 == 0:
                                                return k
                                except ValueError:
                                    pass
                                except TypeError:
                                    pass
                            j -= 1
    return 0


def function_with_dead_code():
    if False:
        print("This will never execute")
        return "dead"
    
    x = 1
    if True:
        return x
    
    return "unreachable"


class ExtremelyLargeClassWithTooManyMethods:
    def method_01(self): pass
    def method_02(self): pass
    def method_03(self): pass
    def method_04(self): pass
    def method_05(self): pass
    def method_06(self): pass
    def method_07(self): pass
    def method_08(self): pass
    def method_09(self): pass
    def method_10(self): pass
    def method_11(self): pass
    def method_12(self): pass
    def method_13(self): pass
    def method_14(self): pass
    def method_15(self): pass
    def method_16(self): pass
    def method_17(self): pass
    def method_18(self): pass
    def method_19(self): pass
    def method_20(self): pass
    def method_21(self): pass
    def method_22(self): pass
    def method_23(self): pass
    def method_24(self): pass
    def method_25(self): pass


class WellDesignedClass:
    def __init__(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def greet(self) -> str:
        return f"Hello, {self.name}!"


def well_designed_function(numbers: List[int]) -> int:
    """Calculate the sum of positive numbers in a list."""
    return sum(num for num in numbers if num > 0)


def another_well_designed_function(data: Dict[str, Any]) -> bool:
    """Check if required keys exist in data dictionary."""
    required_keys = ['name', 'age', 'email']
    return all(key in data for key in required_keys)
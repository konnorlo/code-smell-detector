"""
Synthetic training data
"""

def function_with_dead_code_0_0():
    x = 0
    if False:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_0_1():
    x = 1
    if False:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_0_2():
    x = 2
    if False:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_1_0():
    x = 0
    if 0:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_1_1():
    x = 1
    if 0:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_1_2():
    x = 2
    if 0:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_2_0():
    x = 0
    if None:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_2_1():
    x = 1
    if None:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_2_2():
    x = 2
    if None:
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_3_0():
    x = 0
    if "":
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_3_1():
    x = 1
    if "":
        print("Dead code")
        return "never reached"
    return x


def function_with_dead_code_3_2():
    x = 2
    if "":
        print("Dead code")
        return "never reached"
    return x
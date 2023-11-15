from sympy import *
import math

x = symbols('x')
variables = [x]
constraints = [-x-3, x-3]
penalty_function = [constraint**2 for constraint in constraints]
_function = (2*x+3)*x*(2*x-3)

penalty_gradient = [diff(penalty_function_idx, variable) for penalty_function_idx in penalty_function for variable in variables]
gradient = [diff(_function, variable) for variable in variables]

START = [0]
HOP_LENGTH = 0.01
ACCURACY = 0.001

def get_penatly_ratio(iteration):
    return iteration #iteration * 2

def get_next_step(last_step, hop_length, iteration):
    variables_values = [(variable, last_step[idx]) for idx, variable in enumerate(variables)]
    def calculate_next_coordinate(variable_index, last_coordinate):
        constraints_filled = [constraint.subs(variables_values) for constraint in constraints]
        if (iteration < 3 or iteration > 24): print('constraints', constraints_filled)
        penalty_gradient_filled = [constraint_gradient.subs(variables_values) for constraint_gradient in penalty_gradient]
        if (iteration < 3 or iteration > 24): print("penalty gradient", penalty_gradient_filled)
        gradient_filled = gradient[variable_index].subs(variables_values)
        if (iteration < 3 or iteration > 24): print("gradient filled", gradient_filled)
        filled = gradient_filled + sum([get_penatly_ratio(iteration) * (penalty_gradient_filled[idx] if constraints_filled[idx] > 0 else 0) for idx in range(len(constraints))])
        if (iteration < 3 or iteration > 24): print("filled", filled)
        return last_coordinate - filled * hop_length
    return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(last_step)]

def is_accurate_enough(last, current):
    def get_distance_between_current_and_last(_last, _current):
        squares = map(lambda index: (_current[index] - _last[index])**2, range(len(variables)))
        return math.sqrt(sum(squares))
    distance = get_distance_between_current_and_last(last, current)
    print(distance)
    return distance <= ACCURACY

def find_minimum():
    step_number = 1
    last_step = START
    next_step = get_next_step(START, HOP_LENGTH, 1)
    while not is_accurate_enough(last_step, next_step) and step_number < 1000:
        if (step_number < 3 or step_number > 24): print(f"not yet: {step_number} iteration, {next_step}")
        last_step = next_step
        step_number += 1
        next_step = get_next_step(last_step, HOP_LENGTH, step_number)
    return next_step, step_number

print(find_minimum())
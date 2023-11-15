from sympy import *
import math

x, y = symbols('x y')
variables = [x,y]
_function = (x-1)*(y-1)*x*y
gradient = [diff(_function, variable) for variable in variables]

constraints = [(x-1)**2+y**2-1] #meaning: (x-1)^2 + y^2 should be less or equal 1
penalty_function = [constraint**2 for constraint in constraints]
penalty_gradient = [[diff(penalty_function_idx, variable) for variable in variables] for penalty_function_idx in penalty_function]

START = [2, 2]
STEP_LENGTH = 0.01
ACCURACY = 0.0001


def get_penatly_ratio(iteration):
    return iteration * 0.05

def get_next_step(last_step, iteration):
    variables_values = [(variable, last_step[idx]) for idx, variable in enumerate(variables)]
    constraints_filled = [constraint.subs(variables_values) for constraint in constraints]
    def calculate_next_coordinate(variable_index, last_coordinate):
        penalty_gradient_filled = [constraint_gradient[variable_index].subs(variables_values) for constraint_gradient in penalty_gradient]
        gradient_filled = gradient[variable_index].subs(variables_values)
        penalties = [get_penatly_ratio(iteration) * (penalty_gradient_filled[idx] if constraints_filled[idx] > 0 else 0) for idx in range(len(constraints))]
        filled = gradient_filled + sum(penalties)
        result = last_coordinate - filled * STEP_LENGTH
        return result
      
    return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(last_step)]

def is_accurate_enough(last, current):
    def get_distance_between_steps(_last, _current):
        squares = map(lambda index: (_current[index] - _last[index])**2, range(len(variables)))
        return math.sqrt(sum(squares))
    distance = get_distance_between_steps(last, current)
    return distance <= ACCURACY

def find_minimum():
    step_number = 1
    last_step = START
    next_step = get_next_step(START, step_number)
    while not (is_accurate_enough(last_step, next_step)):
        print(next_step)
        last_step = next_step
        step_number += 1
        next_step = get_next_step(last_step, step_number)
    return step_number, next_step

step_number, final_step = find_minimum()
print(step_number, final_step)
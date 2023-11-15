from sympy import *
import math

x, y = symbols('x y')
variables = [x,y]
_function = 2*(x**2-y)**2 + (1-x)**2

gradient = [diff(_function, variable) for variable in variables]

START = [0,0]
ACCURACY = 0.001

def get_next_step_length(iteration_number):
    return 0.01 * iteration_number**0.5

def get_next_step(last_step, step_length):
    variables_values = [(variable, last_step[idx]) for idx, variable in enumerate(variables)]
    def calculate_next_coordinate(variable_index, last_coordinate):
        gradient_filled = gradient[variable_index].subs(variables_values)
        return last_coordinate - gradient_filled * step_length
    return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(last_step)]

def is_accurate_enough(last, current):
    def get_distance_between_steps(_last, _current):
        squares = map(lambda index: (_current[index] - _last[index])**2, range(len(variables)))
        return math.sqrt(sum(squares))
    distance = get_distance_between_steps(last, current)
    return distance <= ACCURACY
        
def calculate_gradient(point):
    my_substititions = [(variables[idx], point[idx]) for idx in range(len(variables))]
    return [f.subs(my_substititions) for f in gradient]

def find_minimum():
    step_number = 1
    initial_step_length = get_next_step_length(step_number)
    last_step = START
    next_step = get_next_step(START, initial_step_length)
    while not is_accurate_enough(last_step, next_step):
        #print(f"not yet: {step_number} iteration, {next_step}")
        last_step = next_step
        new_step_length = get_next_step_length(step_number)
        next_step = get_next_step(last_step, new_step_length)
        step_number += 1
    return next_step, step_number

print(find_minimum())
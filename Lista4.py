from sympy import *
import math

x, y = symbols('x y')
variables = [x,y]
_function = 2*(x**2-y)**2 + (1-x)**2

gradient = [diff(_function, variable) for variable in variables]

START = [0.5,1]
HOP_LENGTH = 0.05
ACCURACY = 0.01

def calculate_next_hop_length(direction, last_step):
    if all(elem == 0 for elem in direction): return 0
    h = symbols('h')
    my_substititions = [(variables[idx], last_step[idx]-h*direction[idx]) for idx in range(len(variables))]
    direction_function = _function.subs(my_substititions)
    derivative = diff(direction_function, h)
    stationary_points = solveset(derivative, domain=S.Reals)
    stationary_points_values = {elem: direction_function.subs(h, elem) for elem in stationary_points}
    _mininum = min(stationary_points_values, key=stationary_points_values.get)
    return _mininum

def get_next_hop_length(last_step, iteration_number):
    return 0.03 * iteration_number**0.5
    """new_direction = calculate_gradient(last_step)
    return calculate_next_hop_length(new_direction, last_step)"""

def get_next_step(last_step, hop_length):
    variables_values = [(variable, last_step[idx]) for idx, variable in enumerate(variables)]
    def calculate_next_coordinate(variable_index, last_coordinate):
        gradient_filled = gradient[variable_index].subs(variables_values)
        return last_coordinate - gradient_filled * hop_length
    return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(last_step)]

def is_accurate_enough(last, current):
    def get_distance_between_current_and_last(_last, _current):
        squares = map(lambda index: (_current[index] - _last[index])**2, range(len(variables)))
        return math.sqrt(sum(squares))
    distance = get_distance_between_current_and_last(last, current)
    print(distance)
    return distance <= ACCURACY
        
def calculate_gradient(point):
    my_substititions = [(variables[idx], point[idx]) for idx in range(len(variables))]
    return [f.subs(my_substititions) for f in gradient]

def find_minimum():
    step_number = 1
    #initial_hop_length = get_next_hop_length(START, iteration_number=step_number) #changeable hop length
    initial_hop_length = HOP_LENGTH #const hop length
    last_step = START
    next_step = get_next_step(START, initial_hop_length)
    while not is_accurate_enough(last_step, next_step) and step_number < 1000:
        print(f"not yet: {step_number} iteration, {next_step}")
        last_step = next_step
        #new_hop_length = get_next_hop_length(last_step, iteration_number=step_number) #changeable hop length
        new_hop_length = HOP_LENGTH #const hop length
        next_step = get_next_step(last_step, new_hop_length)
        step_number += 1
    return next_step, step_number

print(find_minimum())
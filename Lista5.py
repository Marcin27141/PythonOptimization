from sympy import *
import math

x, y = symbols('x y')
variables = [x,y]
constraints = [(x-1)**2+y**2-1]
penalty_function = [constraint**2 for constraint in constraints]
_function = (x-1)*(y-1)*x*y

penalty_gradient = [[diff(penalty_function_idx, variable) for variable in variables] for penalty_function_idx in penalty_function]
gradient = [diff(_function, variable) for variable in variables]

START = [2, 2]
HOP_LENGTH = 0.025
ACCURACY = 0.001

def get_penatly_ratio(iteration):
    return iteration**0.25 #iteration * 2

def get_next_step(last_step, hop_length, iteration, verbose = False):
    variables_values = [(variable, last_step[idx]) for idx, variable in enumerate(variables)]
    def calculate_next_coordinate(variable_index, last_coordinate):
        constraints_filled = [constraint.subs(variables_values) for constraint in constraints]
        #if verbose: print("constraints filled", constraints_filled)
        penalty_gradient_filled = [constraint_gradient[variable_index].subs(variables_values) for constraint_gradient in penalty_gradient]
        #if verbose: print("penalty gradient filled", penalty_gradient_filled)
        gradient_filled = gradient[variable_index].subs(variables_values)
        #if verbose: print("gradient filled", gradient_filled)
        filled = gradient_filled + sum([get_penatly_ratio(iteration) * (penalty_gradient_filled[idx] if constraints_filled[idx] > 0 else 0) for idx in range(len(constraints))])
        #if verbose: print("filled", filled)
        result = last_coordinate - filled * hop_length
        if verbose: print(f"x{iteration} = {last_step} - {hop_length} * {filled} = {result}")
        return result
    return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(last_step)]

def get_distance(last, current):
    squares = map(lambda index: (current[index] - last[index])**2, range(len(variables)))
    return math.sqrt(sum(squares))

def find_minimum_quietly():
    step_number = 1
    last_step = START
    next_step = get_next_step(START, HOP_LENGTH, 1)
    while not (distance := get_distance(last_step, next_step)) < ACCURACY and step_number < 1000:
        print(next_step)
        last_step = next_step
        step_number += 1
        next_step = get_next_step(last_step, HOP_LENGTH, step_number)
    return step_number, next_step, distance

def find_minimum_with_presentation(_from, _to):
    step_number = 1
    last_step = START
    print(f"step: {HOP_LENGTH}, accuracy: {ACCURACY}, r(i): i")
    print("x0: ", START)
    next_step = get_next_step(START, HOP_LENGTH, 1, True)
    while not (distance := get_distance(last_step, next_step)) < ACCURACY and step_number < 1000:
        if (step_number <= _from or step_number >= _to):
            print(distance)
            print(f"it was {step_number} iteration, {next_step}")
        last_step = next_step
        step_number += 1
        next_step = get_next_step(last_step, HOP_LENGTH, step_number, (step_number <= _from or step_number > _to))
    return next_step, step_number, distance

print(find_minimum_quietly())
#print(find_minimum_with_presentation(2, 50))
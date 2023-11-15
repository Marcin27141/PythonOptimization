from sympy import *
import math

class PenaltyOptimizer:
    def __init__(self):
        self.x, self.y = symbols('x y')
        self.variables = [self.x, self.y]
        self.penalty_function = ((self.x-1)**2+self.y**2-1)**2
        self.penalty_ratio = 0.05
        self.base_function = (self.x-1)*(self.y-1)*self.x*self.y
        self.function = self.base_function + self.penalty_ratio * self.penalty_function
        self.gradient = self.calculate_function_gradient()
        self.START = [2,2]
        self.last_step = self.START
        self.STEP_LENGTH = 0.01
        self.ACCURACY = 0.0001

    def get_penalty_ratio(self, iteration):
        return iteration * 0.05

    def calculate_function_gradient(self):
        return [diff(self.function, variable) for variable in self.variables]

    def update_penalty_function(self, iteration_number):
        self.penalty_ratio = self.get_penalty_ratio(iteration_number)
        self.function = self.base_function + self.penalty_ratio*self.penalty_function
        self.gradient = self.calculate_function_gradient()

    def get_next_step(self):
        variables_values = [(variable, self.last_step[idx]) for idx, variable in enumerate(self.variables)]
        def calculate_next_coordinate(variable_index, last_coordinate):
            gradient_filled = self.gradient[variable_index].subs(variables_values)
            return last_coordinate - gradient_filled * self.STEP_LENGTH
        return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(self.last_step)]

    def is_accurate_enough(self, current):
        def get_distance_between_steps(_last, _current):
            squares = map(lambda index: (_current[index] - _last[index])**2, range(len(self.variables)))
            return math.sqrt(sum(squares))
        distance = get_distance_between_steps(self.last_step, current)
        return distance <= self.ACCURACY
        
    def find_minimum(self):
        step_number = 1
        next_step = self.get_next_step()
        print(next_step)
        while not self.is_accurate_enough(next_step):
            print(next_step)
            step_number += 1
            self.last_step = next_step
            self.update_penalty_function(step_number)
            next_step = self.get_next_step()
        return next_step, step_number

optimizer = PenaltyOptimizer()
print(optimizer.find_minimum())
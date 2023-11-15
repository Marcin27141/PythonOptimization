from sympy import *
import math

class PenaltyOptimizer:
    def __init__(self):
        self.x, self.y = symbols('x y')
        self.variables = [self.x, self.y]
        self.penalty_function = ((self.x-1)**2+self.y**2-1)**2
        self.penalty_ratio = 2
        self.base_function = (self.x-1)*(self.y-1)*self.x*self.y
        self.function = self.base_function + self.penalty_ratio * self.penalty_function
        self.gradient = self.calculate_gradient_from_function()
        self.START = [2,2]
        self.last_step = self.START
        self.step_length = 0
        self.ACCURACY = 0.0001

    def calculate_gradient_from_function(self):
        return [diff(self.function, variable) for variable in self.variables]

    def set_next_step_length(self, iteration_number):
        #self.step_length = 0.03 * iteration_number**0.5
        return 0.01

    def get_next_step(self):
        variables_values = [(variable, self.last_step[idx]) for idx, variable in enumerate(self.variables)]
        def calculate_next_coordinate(variable_index, last_coordinate):
            gradient_filled = self.gradient[variable_index].subs(variables_values)
            return last_coordinate - gradient_filled * self.step_length
        return [calculate_next_coordinate(idx, coordinate) for idx, coordinate in enumerate(self.last_step)]

    def is_accurate_enough(self, current):
        def get_distance_between_steps(_last, _current):
            squares = map(lambda index: (_current[index] - _last[index])**2, range(len(self.variables)))
            return math.sqrt(sum(squares))
        distance = get_distance_between_steps(self.last_step, current)
        return distance <= self.ACCURACY
        
    def calculate_gradient(self, point):
        my_substititions = [(self.variables[idx], point[idx]) for idx in range(len(self.variables))]
        return [f.subs(my_substititions) for f in self.gradient]

    def find_minimum(self):
        step_number = 1
        self.set_next_step_length(step_number)
        next_step = self.get_next_step()
        while not self.is_accurate_enough(next_step):
            print(f"not yet: {step_number} iteration, {next_step}")
            self.last_step = next_step
            self.penalty_ratio *= 2
            self.function = self.base_function + self.penalty_ratio*self.penalty_function
            self.gradient = self.calculate_gradient_from_function()
            self.set_next_step_length(step_number)  
            next_step = self.get_next_step()
            step_number += 1
        return next_step, step_number

optimizer = PenaltyOptimizer()
print(optimizer.find_minimum())
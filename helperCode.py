import operator

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


plus = Infix(lambda x,y: x+y)
times = Infix(lambda x,y: x*y)
# plus = Infix(operator.add)
# times = Infix(operator.mul)


print(2 |plus| (4 |times| 5))

# __or__ returns result of Math, so maybe should return Math instead.
# plus is type Infix. Infixes are basically functions???



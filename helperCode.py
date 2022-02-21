# # Variables and Constants are Terms.
# class Term():
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value
#         self.children = []                  # The children are the variables that will change if this term has a value.
#     # This checks if they *can* be equal.
#     def __eq__(self, other):
#         return self.value == other.value or not self or not other
#     def __bool__(self):
#         return self.value != "Undefined"    # A term is false it if has no value.
#     def __repr__(self):
#         return repr(self.name + " = " + str(self.value))    
#     def __str__(self):
#         return str(self.value)
#     def __hash__(self):
#         return hash(repr(self))
    
        
# class Var(Term):
#     def __init__(self, name, value = "Undefined"):
#         super().__init__(name = name, value = value)    # Initialize the Var.

# X = 4
# H = exec("X + 3")
# print(H)

lst = [1]

# test = lst[1:] if lst[1:] else "banana"

print(lst[-2])
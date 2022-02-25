# import re
# # # Variables and Constants are Terms.
# # class Term():
# #     def __init__(self, name, value):
# #         self.name = name
# #         self.value = value
# #         self.children = []                  # The children are the variables that will change if this term has a value.
# #     # This checks if they *can* be equal.
# #     def __eq__(self, other):
# #         return self.value == other.value or not self or not other
# #     def __bool__(self):
# #         return self.value != "Undefined"    # A term is false it if has no value.
# #     def __repr__(self):
# #         return repr(self.name + " = " + str(self.value))    
# #     def __str__(self):
# #         return str(self.value)
# #     def __hash__(self):
# #         return hash(repr(self))
    
        
# # class Var(Term):
# #     def __init__(self, name, value = "Undefined"):
# #         super().__init__(name = name, value = value)    # Initialize the Var.

# # X = 4
# # H = exec("X + 3")
# # print(H)

# # How to split and keep delimeters.
# # 1: To keep delimeter, put () around what you are searching for.
# # 2: To split on multiple things, use |.
# # str = "X =\= 4"
# str = "5 is 4"

# # Remove spaces.
# # str = str.replace(" ", "")

# # lst = re.split(r'(=:=| is |=\\=|<|=<|>|>=)', str)
# lst = re.split(r'( is )', str)
# print(lst)

x = []

if x:
    print("hi")
else:
    print("bye")
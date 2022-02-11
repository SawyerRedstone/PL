# # class Term():
# #     def __init__(self, value, name):
# #         self.value = value
# #         self.name = name
# #     def __add__(self, addend):
# #         if isinstance(addend, Term):
# #             # If value.isdigit(), do int(value). Else, return false.
# #             return Term(self.value + addend.value, "Math")
# #             # return self.num_val + addend.num_val
# #         return Term(self.value + addend, "Math") 
# #         # return self.num_val + addend
# #     # def __radd__(self, addend):
# #     #     if isinstance(addend, Term):
# #     #         # If value.isdigit(), do int(value). Else, return false.
# #     #         return Term(self.value + addend.value, "Math")
# #     #         # return self.num_val + addend.num_val
# #     #     return Term(self.value + addend, "Math") 
# #     #     # return self.num_val + addend
        
# #     def __str__(self):
# #         return str(self.value)


# # myFoo = Term(18, "bob")
# # # res = eval("myFoo + 2")
# # res = eval("myFoo + 2")

# # print(res) 

# # # myFoo = Term(10, "bob")
# # # # numFoo = Term("22 + myFoo", "num")
# # # numFoo = Term("myFoo + 22", "num")


# # # # res = eval("myFoo + numFoo")
# # # # res = eval("myFoo")
# # # res = eval("numFoo.value")



# # # # res = eval(2) <- fails, since 2 isn't a string.
# # # # res = eval("myFoo")
# # # print(res) 



# # # class Foo():
# # #     def __init__(self, num):
# # #         self.num_val = num
# # #     def __add__(self, addend):
# # #         if isinstance(addend, Foo):
# # #             return Foo(self.num_val + addend.num_val)
# # #         return Foo(self.num_val + addend) 
# # #     def __str__(self):
# # #         return f"{self.num_val}"

# # # myFoo = Foo(18)
# # # res = eval("myFoo + 2")
# # # print(res) 

# class Foo():
#     def __init__(self, num):
#         self.num_val = num
#     # def __add__(self, addend):
#     #     if isinstance(addend, Foo):
#     #         return Foo(self.num_val + addend.num_val)
#     #     return Foo(self.num_val + addend) 
#     def __str__(self):
#         # return f"{self.num_val}"
#         return str(eval(self.num_val))

# myFoo = Foo("2+2")
# res = eval("myFoo")
# print(res)

print(float(2.5))
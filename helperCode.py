class Foo():
    def __init__(self, num, name):
        self.num_val = num
        self.name = name
    def __add__(self, addend):
        if isinstance(addend, Foo):
            # return Foo(self.num_val + addend.num_val, "Math")
            return self.num_val + addend.num_val
        # return Foo(self.num_val + addend, "Math") 
        return self.num_val + addend
    def __str__(self):
        return str(self.num_val)

numFoo = Foo(22, "num")
myFoo = Foo(18, "bob")
res = eval("myFoo +   numFoo")
# res = eval("myFoo")
print(res) 
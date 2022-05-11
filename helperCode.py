# This takes a string of math and turns it into a list of numbers and operators
def mathToList(math):
    math = math.replace(" ", "")
    math = math.replace("+", " + ")
    math = math.replace("-", " - ")
    math = math.replace("*", " * ")
    math = math.replace("/", " / ")
    math = math.replace("(", " ( ")
    math.replace(")", " ) ")
    math = math.split()

    # math = [i if i in "+-*/()" else i.value for i in math]
    for i in range(len(math)):
        if math[i] in "+-*/()":
            continue
        else:
            try:
                math[i] = math[i].value
            except:
                raise ValueError("Invalid input")
    return math

x = mathToList("1 + (2 * 3)")
print(x)
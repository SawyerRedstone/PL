# PL code to accompany PL_Documentation.pdf

from PL import *


############ Adding to the knowledge base. ############

# Define all the predicates that will be used.
male = Predicate("male")
female = Predicate("female")
child = Predicate("child")
parent = Predicate("parent")
mother = Predicate("mother")
ancestor = Predicate("ancestor")
count = Predicate("count")
write_var = Predicate("write_var")
write_var2 = Predicate("write_var2")
always_true = Predicate("always_true")

# We can save future typing by defining Vars here.
A = Var("A")
B = Var("B")
C = Var("C")

# Here we define our facts.
male.add([Const("Sawyer")])
male.add([Const("Michael")])
female.add([Const("Rachel")])
female.add([Const("Naomi")])
child.add([Const("Sawyer"), Const("Michael")])
child.add([Const("Sawyer"), Const("Rachel")])
child.add([Const("Rachel"), Const("Naomi")])
always_true.add([])

# Here we define our rules.
parent.add([A, B], [Goal(child, B, A)])
mother.add([A, B], [Goal(female, A), Goal(parent, A, B)])

ancestor.add([A, B], [Goal(parent, A, B)])
ancestor.add([A, B], [Goal(parent, A, C), Goal(ancestor, C, B)])

count.add([A, A])
count.add([A, C], [Goal(equals, B, A + Const(1)), Goal(count, B, C)])

write_var.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A)])

write_var2.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A), fail])


################## QUERIES ##################

# Variable used in queries
X = Var("X")
Y = Var("Y")

###### Uncomment these queries one by one to test their results. ######
# success = tryGoal(Goal(male, X))
# success = tryGoal(Goal(female, X))
# success = tryGoal(Goal(child, X, Y))
# success = tryGoal(Goal(parent, X, Y))
# success = tryGoal(Goal(mother, X, Y))
# success = tryGoal(Goal(ancestor, X, Y))
# success = tryGoal(Goal(count, Const(0), X))   # As this will produce infinite results, it is recommended not to display all solutions.
# success = tryGoal(Goal(write_var, X))
# success = tryGoal(Goal(write_var2, X))
# success = tryGoal(Goal(always_true))

######### Displaying Results #########

# This will display all results. 
# To change how many results display, comment these lines and uncomment one of the options below.
for s in success:
    print(s)

# # If you wish to choose how many results appear, uncomment these lines. Default is 5.
# for _ in range(5):
#     print(next(success))

# # To display only the first result, uncomment these lines.
# print(next(success))





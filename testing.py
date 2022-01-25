# This file is used for internal testing.

# from PL import *
from Experimenting import *


################### Testing #####################

# First we define all the predicates that will be tested.
male = Predicate("male")
female = Predicate("female")
child = Predicate("child")
parent = Predicate("parent")
father = Predicate("father")
mother = Predicate("mother")
ancestor = Predicate("ancestor")
count = Predicate("count")
just_ate = Predicate("just_ate")
is_digesting = Predicate("is_digesting")
always_true = Predicate("always_true")
write_var = Predicate("write_var")

#### facts/rules ####

male.add([Const("bob")])
male.add([Const("john")])
male.add([Const("ben")])
male.add([Const("martin")])
male.add([Const("edmund")])
male.add([Const("david")])
male.add([Const("isidore")])
male.add([Const("william")])
male.add([Const("ferdinand")])
male.add([Const("morris")])
male.add([Const("alphonse")])
male.add([Const("jiri")])


female.add([Const("kathryn")])
female.add([Const("beatrice")])
female.add([Const("rachel")])
female.add([Const("lillian")])
female.add([Const("alice")])
female.add([Const("rosa")])
female.add([Const("marjorie")])
female.add([Const("emma")])
female.add([Const("nellie")])
female.add([Const("eva")])
female.add([Const("bertha")])
female.add([Const("fergie")])


child.add([Const("bob"), Const("john")])
child.add([Const("bob"), Const("kathryn")])
child.add([Const("beatrice"), Const("john")])
child.add([Const("beatrice"), Const("kathryn")])
child.add([Const("john"), Const("ben")])
child.add([Const("john"), Const("rachel")])
child.add([Const("lillian"), Const("ben")])
child.add([Const("lillian"), Const("rachel")])
child.add([Const("kathryn"), Const("rosa")])
child.add([Const("kathryn"), Const("martin")])
child.add([Const("alice"), Const("martin")])
child.add([Const("alice"), Const("rosa")])
child.add([Const("ferdinand"), Const("martin")])
child.add([Const("ferdinand"), Const("fergie")])
child.add([Const("marjorie"), Const("edmund")])
child.add([Const("marjorie"), Const("lillian")])
child.add([Const("david"), Const("lillian")])
child.add([Const("david"), Const("edmund")])
child.add([Const("ben"), Const("isidore")])
child.add([Const("ben"), Const("bertha")])
child.add([Const("william"), Const("isidore")])
child.add([Const("william"), Const("bertha")])
child.add([Const("emma"), Const("isidore")])
child.add([Const("emma"), Const("bertha")])
child.add([Const("morris"), Const("alphonse")])
child.add([Const("morris"), Const("emma")])
child.add([Const("nellie"), Const("alphonse")])
child.add([Const("nellie"), Const("emma")])
child.add([Const("eva"), Const("alphonse")])
child.add([Const("eva"), Const("emma")])
child.add([Const("jiri"), Const("alphonse")])
child.add([Const("jiri"), Const("emma")])


just_ate.add([Const("deer"), Const("grass")])
just_ate.add([Const("tiger"), Const("deer")])


# Save typing by defining Vars on top.
A = Var("A")
B = Var("B")
C = Var("C")


# is_digesting(A, B) :- just_ate(A, B).
# is_digesting(A, B) :- just_ate(A, C), is_digesting(C, B).
is_digesting.add([A, B], [Goal(just_ate, A, B)])
is_digesting.add([A, B], [Goal(just_ate, A, C), Goal(is_digesting, C, B)])

# parent(michael, sawyer).
# parent(A, B) :- child(B, A).
parent.add([Const("Michael"), Const("Sawyer")])
parent.add([A, B], [Goal(child, B, A)])
# parent.add([Var("A"), Var("B")], [Goal(child, Var("B"), Var("A"))])     # Test success!


# father(A, B) :- male(A), parent(A, B).
father.add([A, B], [Goal(male, A), Goal(parent, A, B)])


# # father(B, A) :- male(B), parent(B, A).
# father.add([B, A], [Goal(male, B), Goal(parent, B, A)])              # Test success!

# mother(A, B) :- female(A), parent(A, B).
# mother(lily).
# mother(ella).
mother.add([A, B], [Goal(female, A), Goal(parent, A, B)])
mother.add([Const("Lily")])
mother.add([Const("Ella")])


# ancestor(A, B) :- parent(A, B).
# ancestor(A, B) :- parent(A, C), ancestor(C, B).
ancestor.add([A, B], [Goal(parent, A, B)])
ancestor.add([A, B], [Goal(parent, A, C), Goal(ancestor, C, B)])

# count(A, A).
# count(A, C) :- B is A+1, count(B, C).
count.add([A, A])
count.add([A, C], [Goal(equals, B, A + Const(1)), Goal(count, B, C)])

# write_var(A) :- A is 6 + 2, write(A), fail.
write_var.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A), fail])

# write_var(A) :- A is 6 + 2, write(A).
# write_var.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A)])

always_true.add()

##########################################

### All tests below succeed! ###

X = Var("X")
Y = Var("Y")

# # ?- male(X).
# # Becomes:
# success = tryGoal(Goal(male, X))

# # ?- child(X, Y).
# success = tryGoal(Goal(child, X, Y))

# # ?- parent(X, Y).
# success = tryGoal(Goal(parent, X, Y))

# # ?- father(X, Y).
success = tryGoal(Goal(father, X, Y))

# # ?- child(X, ben).
# success = tryGoal(Goal(child, X, Const("ben")))

# # ?- parent(john, X).
# success = tryGoal(Goal(parent, Const("john"), X))

# # ?- just_ate(X, Y).
# success = tryGoal(Goal(just_ate, X, Y))


# # ?- write_var(A)
# success = tryGoal(Goal(write_var, X))

# # ?- X is 2 + 4.
# # ?- is(X, 2 + 4).
# success = tryGoal(Goal(equals, X, Const(2)+Const(4)))

# # ?- 6 is 2 + 4.
# success = tryGoal(Goal(equals, Const(6), Const(2) + Const(4)))

# # ?- 6 is 2 + "hi".
# success = tryGoal(Goal(equals, X, Const(2) + Const("hi")))

############# Arity of 0 #################

# # ?- fail.
# success = tryGoal(fail)

# # ?- always_true.
# success = tryGoal(Goal(always_true))

################ Recursion ##################

# # ?- is_digesting(tiger, grass).
# success = tryGoal(Goal(is_digesting, Const("tiger"), Const("grass")))

# # ?- is_digesting(X, Y).
# success = tryGoal(Goal(is_digesting, X, Y))

# # ?- count(0, X).
# success = tryGoal(Goal(count, Const(0), X))

# # ?- ancestor(X, bob).
# success = tryGoal(Goal(ancestor, X, Const("bob")))

######### Different arities for same predicate ###########
# success = tryGoal(Goal(mother))
# success = tryGoal(Goal(mother, X))
# success = tryGoal(Goal(mother, X, Y))

########## Using the Write goal. #######
# success = tryGoal(Goal(write, Const("hi")))
# success = tryGoal(Goal(write_var, X))

########################## Check results here! ##########################


#### To see all results #####
for s in success:
    print(s)


# ### To see only some results ####
# for _ in range(10):
#     print(next(success))

#### Alternatives for specific cases ####
# for i in tryGoal(Goal(parent, X, Y)):
#     print(i)

# success = tryGoal(Goal(parent, X, Y))
# print(next(success))
# print(next(success))

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
collatz = Predicate("collatz")
member = Predicate("member")

#### facts/rules ####


male.add(["bob"])
male.add(["john"])
male.add(["ben"])
male.add(["martin"])
male.add(["edmund"])
male.add(["david"])
male.add(["isidore"])
male.add(["william"])
male.add(["ferdinand"])
male.add(["morris"])
male.add(["alphonse"])
male.add(["jiri"])


female.add(["kathryn"])
female.add(["beatrice"])
female.add(["rachel"])
female.add(["lillian"])
female.add(["alice"])
female.add(["rosa"])
female.add(["marjorie"])
female.add(["emma"])
female.add(["nellie"])
female.add(["eva"])
female.add(["bertha"])
female.add(["fergie"])


child.add(["bob", "john"])
child.add(["bob", "kathryn"])
child.add(["beatrice", "john"])
child.add(["beatrice", "kathryn"])
child.add(["john", "ben"])
child.add(["john", "rachel"])
child.add(["lillian", "ben"])
child.add(["lillian", "rachel"])

# child.add([Const("kathryn"), Const("rosa")])
# child.add([Const("kathryn"), Const("martin")])
# child.add([Const("alice"), Const("martin")])
# child.add([Const("alice"), Const("rosa")])
# child.add([Const("ferdinand"), Const("martin")])
# child.add([Const("ferdinand"), Const("fergie")])
# child.add([Const("marjorie"), Const("edmund")])
# child.add([Const("marjorie"), Const("lillian")])
# child.add([Const("david"), Const("lillian")])
# child.add([Const("david"), Const("edmund")])
# child.add([Const("ben"), Const("isidore")])
# child.add([Const("ben"), Const("bertha")])
# child.add([Const("william"), Const("isidore")])
# child.add([Const("william"), Const("bertha")])
# child.add([Const("emma"), Const("isidore")])
# child.add([Const("emma"), Const("bertha")])
# child.add([Const("morris"), Const("alphonse")])
# child.add([Const("morris"), Const("emma")])
# child.add([Const("nellie"), Const("alphonse")])
# child.add([Const("nellie"), Const("emma")])
# child.add([Const("eva"), Const("alphonse")])
# child.add([Const("eva"), Const("emma")])
# child.add([Const("jiri"), Const("alphonse")])
# child.add([Const("jiri"), Const("emma")])


just_ate.add(["deer", "grass"])
just_ate.add(["tiger", "deer"])


# # is_digesting(A, B) :- just_ate(A, B).
# # is_digesting(A, B) :- just_ate(A, C), is_digesting(C, B).
is_digesting.add(["A", "B"], [[just_ate, "A", "B"]])
is_digesting.add(["A", "B"], [[just_ate, "A", "C"], [is_digesting, "C", "B"]])


# # parent(michael, sawyer).
# # parent(A, B) :- child(B, A).
# parent.add([Const("Michael"), Const("Sawyer")])
# parent.add([A, B], [Goal(child, B, A)])
# # parent.add([Var("A"), Var("B")], [Goal(child, Var("B"), Var("A"))])     # Test success!


# # father(A, B) :- male(A), parent(A, B).
# father.add([A, B], [Goal(male, A), Goal(parent, A, B)])


# # # father(B, A) :- male(B), parent(B, A).
# # father.add([B, A], [Goal(male, B), Goal(parent, B, A)])              # Test success!

# # mother(A, B) :- female(A), parent(A, B).
# # mother(lily).
# # mother(ella).
# mother.add([A, B], [Goal(female, A), Goal(parent, A, B)])
# mother.add([Const("Lily")])
# mother.add([Const("Ella")])


# # ancestor(A, B) :- parent(A, B).
# # ancestor(A, B) :- parent(A, C), ancestor(C, B).
# ancestor.add([A, B], [Goal(parent, A, B)])
# ancestor.add([A, B], [Goal(parent, A, C), Goal(ancestor, C, B)])

# # count(A, A).
# # count(A, C) :- B is A+1, count(B, C).
# count.add([A, A])
# count.add([A, C], [Goal(equals, B, A + Const(1)), Goal(count, B, C)])

# # write_var(A) :- A is 6 + 2, write(A), fail.
# write_var.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A), fail])

# # write_var(A) :- A is 6 + 2, write(A).
# # write_var.add([A], [Goal(equals, A, Const(6)+Const(2)), Goal(write, A)])

# always_true.add()

# # FAILED ???
# # collatz(A, A).
# # collatz(B, A) :- 0 is mod(B, 2), C is B / 2, collatz(C, A).
# # collatz(B, A) :- 1 is mod(B, 2), C is 3 * B + 1, collatz(C, A).
# collatz.add([A, A])
# collatz.add([B, A], [Goal(equals, Const(0), B % Const(2)), Goal(equals, C, B / Const(2)), Goal(collatz, C, A)])
# collatz.add([B, A], [Goal(equals, Const(1), B % Const(2)), Goal(equals, C, Const(3) * B + Const(1)), Goal(collatz, C, A)])

##########################################

### All tests below succeed! ###


# # ?- male(X).
# # Becomes:
success = solve([male, "X"])

# # ?- child(X, Y).
# success = tryGoal(Goal(child, X, Y))
# success = tryGoal(Goal(child, Var("X"), Var("X")))    # It thinks these Xs are different! ???


# # ?- parent(X, Y).
# success = tryGoal(Goal(parent, X, Y))

# # ?- father(X, Y).
# success = tryGoal(Goal(father, X, Y))

# # ?- child(X, ben).
# success = tryGoal(Goal(child, X, Const("ben")))

# # ?- parent(john, X).
# success = tryGoal(Goal(parent, Const("john"), X))

# # ?- just_ate(X, Y).
# success = tryGoal(Goal(just_ate, X, Y))


# # ?- write_var(X)
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
success = solve([is_digesting, "tiger", "grass"])


# # ?- is_digesting(X, Y).
# success = tryGoal(Goal(is_digesting, X, Y))

# # ?- count(0, X).
# success = tryGoal(Goal(count, Const(0), X))

# # ?- ancestor(X, bob).
# success = tryGoal(Goal(ancestor, X, Const("bob")))

# collatz(10, X).   # Fails. ???
# success = tryGoal(Goal(collatz, Const(10), X))

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
# for _ in range(5):
#     print(next(success))

#### Alternatives for specific cases ####
# for i in tryGoal(Goal(parent, X, Y)):
#     print(i)

# success = tryGoal(Goal(parent, X, Y))
# print(next(success))
# print(next(success))

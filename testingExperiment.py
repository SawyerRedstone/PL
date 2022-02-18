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
listTest = Predicate("list_test")
inboth = Predicate("inboth")
increment_all = Predicate("increment_all")

# #### facts/rules ####

# male.add(["bob"])
# male.add(["john"])
# male.add(["ben"])
# male.add(["martin"])
# male.add(["edmund"])
# male.add(["david"])
# male.add(["isidore"])
# male.add(["william"])
# male.add(["ferdinand"])
# male.add(["morris"])
# male.add(["alphonse"])
# male.add(["jiri"])


# female.add(["kathryn"])
# female.add(["beatrice"])
# female.add(["rachel"])
# female.add(["lillian"])
# female.add(["alice"])
# female.add(["rosa"])
# female.add(["marjorie"])
# female.add(["emma"])
# female.add(["nellie"])
# female.add(["eva"])
# female.add(["bertha"])
# female.add(["fergie"])


# child.add(["bob", "john"])
# child.add(["bob", "kathryn"])
# child.add(["beatrice", "john"])
# child.add(["beatrice", "kathryn"])
# child.add(["john", "ben"])
# child.add(["john", "rachel"])
# child.add(["lillian", "ben"])
# child.add(["lillian", "rachel"])
# child.add(["kathryn", "rosa"])
# child.add(["kathryn", "martin"])
# child.add(["alice", "martin"])
# child.add(["alice", "rosa"])
# child.add(["ferdinand", "martin"])
# child.add(["ferdinand", "fergie"])
# child.add(["marjorie", "edmund"])
# child.add(["marjorie", "lillian"])
# child.add(["david", "lillian"])
# child.add(["david", "edmund"])
# child.add(["ben", "isidore"])
# child.add(["ben", "bertha"])
# child.add(["william", "isidore"])
# child.add(["william", "bertha"])
# child.add(["emma", "isidore"])
# child.add(["emma", "bertha"])
# child.add(["morris", "alphonse"])
# child.add(["morris", "emma"])
# child.add(["nellie", "alphonse"])
# child.add(["nellie", "emma"])
# child.add(["eva", "alphonse"])
# child.add(["eva", "emma"])
# child.add(["jiri", "alphonse"])
# child.add(["jiri", "emma"])


# just_ate.add(["deer", "grass"])
# just_ate.add(["tiger", "deer"])


# # is_digesting(A, B) :- just_ate(A, B).
# # is_digesting(A, B) :- just_ate(A, C), is_digesting(C, B).
# is_digesting.add(["A", "B"], [[just_ate, "A", "B"]])
# is_digesting.add(["A", "B"], [[just_ate, "A", "C"], [is_digesting, "C", "B"]])


# # parent(michael, sawyer).
# # parent(A, B) :- child(B, A).
# parent.add(["michael", "sawyer"])
# # parent.add(["A", "B"], [[child, "B", "A"]])
# parent.add(["A", "B"], [child("B", "A")])



# # father(A, B) :- male(A), parent(A, B).
# father.add(["A", "B"], [[male, "A"], [parent, "A", "B"]])


# # # mother(A, B) :- female(A), parent(A, B).
# # # mother(lily).
# # # mother(ella).
# mother.add(["A", "B"], [[female, "A"], [parent, "A", "B"]])
# mother.add(["lily"])
# mother.add(["ella"])


# # # ancestor(A, B) :- parent(A, B).
# # # ancestor(A, B) :- parent(A, C), ancestor(C, B).
# ancestor.add(["A", "B"], [[parent, "A", "B"]])
# ancestor.add(["A", "B"], [[parent, "A", "C"], [ancestor, "C", "B"]])

# # # count(A, A).
# # # count(A, C) :- B is A+1, count(B, C).
# count.add(["A", "A"])
# count.add(["A", "C"], [[equals, "B", "A + 1"], [count, "B", "C"]])

# # # write_var(A) :- A is 6 + 2, write(A), fail.
# write_var.add(["A"], [[equals, "A", "6 + 2"], [write, "A"], [fail]])

# always_true.add()

# # # collatz(A, A).
# # # collatz(B, A) :- 0 is mod(B, 2), C is B / 2, collatz(C, A).
# # # collatz(B, A) :- 1 is mod(B, 2), C is 3 * B + 1, collatz(C, A).
# collatz.add(["A", "A"])
# collatz.add(["B", "A"], [[equals, "0", "B % 2"], [equals, "C", "B / 2"], [collatz, "C", "A"]])
# collatz.add(["B", "A"], [[equals, "1", "B % 2"], [equals, "C", "3 * B + 1"], [collatz, "C", "A"]])

# listTest.add([["bob", "carol", "ted", "alice"]])

# # inboth(A, B, X) :- member(X, A), member(X, B).
# inboth.add(["A", "B", "X"], [[member, "X", "A"], [member, "X", "B"]])
# # inboth.add(["A", "B", "X"], [[member("X", "A")], [member("X", "B")]])


# # increment_all([], X) :- X = [].
# # increment_all([H|T], X) :- Y is H + 1, increment_all(T, Z), X = [Y|Z].
# increment_all.add([[], "X"], ["X = []"])

# ##########################################


# ### All tests below succeed! ###

# # success = male("X")
# # print(male("X"))

# # ?- inboth([green, red, orange], [apple, orange, pear], orange).
# # success = solve([inboth, ["green", "red", "orange"], ["apple", "orange", "pear"], "orange"])
# # success = inboth(["green", "red", "orange"], ["apple", "orange", "pear"], "orange")

# # ?- inboth([1, 2, 3, 4], [2, 5, 6, 1], X).
# # success = solve([inboth, ["1", "2", "3", "4"], ["2", "5", "6", "1"], "X"])

# # success = solve([listTest, ["X", "|", "Y"]])
# # success = solve([listTest, ["bob", "carol", "ted", "ali"]])
# # success = solve([listTest, ["bob", "carol", "ted", "alice"]])

# # # ?- member(X, [bob, apple, shirt, pip]).
# # success = solve([member, "X", ["bob", "apple", "shirt", "pip"]])

# # # ?- male(X).
# # # Becomes:
# # success = solve([male, "X"])

# # # ?- child(X, Y).
# # success = solve([child, "X", "Y"])
# # success = child("X", "Y")

# # # ?- parent(X, Y).
# # success = solve([parent, "X", "Y"])
# success = parent("X", "Y")

# # # ?- father(X, Y).
# # success = solve([father, "X", "Y"])

# # # ?- child(X, ben).
# # success = solve([child, "X", "ben"])

# # # ?- parent(john, X).
# # success = solve([parent, "john", "X"])

# # # ?- just_ate(X, Y).
# # success = solve([just_ate, "X", "Y"])

# # # ?- write(hi)
# # success = solve([write, "hi"])

# # # ?- write_var(X)
# # success = solve([write_var, "X"])

# # # ?- X is 2 + 4.
# # # ?- is(X, 2 + 4).
# # success = solve([equals, "X", "2 + 4"])

# # # ?- 6 is 2 + 4.
# # success = solve([equals, "6", "2 + 4"])

# # # ?- 6 is 2 + 8.
# # success = solve([equals, "6", "2 + 8"])

# # # ?- 6 is 2 + "hi".
# # success = solve([equals, "X", "2 + hi"])

# ############# Arity of 0 #################

# # # ?- fail.
# # success = solve([fail])

# # # ?- always_true.
# # success = solve([always_true])

# ################ Recursion ##################

# # # ?- is_digesting(tiger, grass).
# # success = solve([is_digesting, "tiger", "grass"])


# # # ?- is_digesting(X, Y).
# # success = solve([is_digesting, "X", "Y"])


# # # ?- count(0, X).
# # success = solve([count, "0", "X"])

# # # ?- ancestor(X, bob).
# # success = solve([ancestor, "X", "bob"])

# # collatz(10, X).
# # success = solve([collatz, "10", "X"])

# ######### Different arities for same predicate ###########
# # success = solve([mother])
# # success = solve([mother, "X"])
# # success = solve([mother, "X", "Y"])

# ########## Using the Write goal. #######
# # success = solve([write, "hi"])
# # success = solve([write_var, "X"])

# ########################## Check results here! ##########################

+just_ate("deer", "grass")
+just_ate("tiger", "deer")

# success = -just_ate("X", "Y")

# # is_digesting(A, B) :- just_ate(A, B).
# # is_digesting(A, B) :- just_ate(A, C), is_digesting(C, B).

is_digesting("A", "B") >> [just_ate("A", "B")]
is_digesting("A", "B") >> [just_ate("A", "C"), is_digesting("C", "B")]

# # # ?- is_digesting(tiger, grass).
# success = -is_digesting("tiger", "grass")


# # # ?- is_digesting(X, Y).
# # success = solve([is_digesting, "X", "Y"])
success = -is_digesting("X", "Y")



### To see all results #####
for s in success:
    print(s)

# # ### To see all results #####
# # for s in male("X"):
# #     print(s)


# # ### To see only some results ####
# # for _ in range(5):
# #     print(next(success))

# # #### Alternatives for specific cases ####
# # for i in solve([parent, "X", "Y"]):
# #     print(i)

# # success = solve([parent, "X", "Y"])
# # print(next(success))
# # print(next(success))


# just_ate.add(["deer", "grass"])
# just_ate.add(["tiger", "deer"])




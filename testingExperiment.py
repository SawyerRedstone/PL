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
sibling = Predicate("sibling")
uncle = Predicate("uncle")
aunt = Predicate("aunt")
ancestor = Predicate("ancestor")
first_cousin = Predicate("first_cousin")
collatz = Predicate("collatz")
inboth = Predicate("inboth")
increment_all = Predicate("increment_all")
just_ate = Predicate("just_ate")
is_digesting = Predicate("is_digesting")
count = Predicate("count")
always_true = Predicate("always_true")
basicList = Predicate("basicList")
merge = Predicate("merge")

# #### facts/rules ####

+male(C.bob)
+male(C.john)
+male(C.ben)
+male(C.martin)
+male(C.edmund)
+male(C.david)
+male(C.isidore)
+male(C.william)
+male(C.ferdinand)
+male(C.morris)
+male(C.alphonse)
+male(C.jiri)
+female(C.kathryn)
+female(C.beatrice)
+female(C.rachel)
+female(C.lillian)
+female(C.alice)
+female(C.rosa)
+female(C.marjorie)
+female(C.emma)
+female(C.nellie)
+female(C.eva)
+female(C.bertha)
+female(C.fergie)

# A is the child of B
+child(C.bob, C.john)
+child(C.bob, C.kathryn)
+child(C.beatrice, C.john)
+child(C.beatrice, C.kathryn)
+child(C.john, C.ben)
+child(C.john, C.rachel)
+child(C.lillian, C.ben)
+child(C.lillian, C.rachel)
+child(C.kathryn, C.rosa)
+child(C.kathryn, C.martin)
+child(C.alice, C.martin)
+child(C.alice, C.rosa)
+child(C.ferdinand, C.martin)
+child(C.ferdinand, C.fergie)
+child(C.marjorie, C.edmund)
+child(C.marjorie, C.lillian)
+child(C.david, C.lillian)
+child(C.david, C.edmund)
+child(C.ben, C.isidore)
+child(C.ben, C.bertha)
+child(C.william, C.isidore)
+child(C.william, C.bertha)
+child(C.emma, C.isidore)
+child(C.emma, C.bertha)
+child(C.morris, C.alphonse)
+child(C.morris, C.emma)
+child(C.nellie, C.alphonse)
+child(C.nellie, C.emma)
+child(C.eva, C.alphonse)
+child(C.eva, C.emma)
+child(C.jiri, C.alphonse)
+child(C.jiri, C.emma)

parent(V.A, V.B) >> [child(V.B, V.A)]

father(V.A, V.B) >> [male(V.A), parent(V.A, V.B)]
mother(V.A, V.B) >> [female(V.A), parent(V.A, V.B)]

# sibling(V.A, V.B) >> [parent(V.X, V.A), parent(V.X, V.B), V.A \= V.B]

# uncle(V.A, V.B) >> [parent(V.X, V.B), sibling(V.A, V.X), male(V.A)]
# aunt(V.A, V.B) >> [parent(V.X, V.B), sibling(V.A, V.X), female(V.A)]

ancestor(V.A, V.B) >> [parent(V.A, V.B)]
ancestor(V.A, V.B) >> [parent(V.A, V.X), ancestor(V.X, V.B)]

# first_cousin(V.A, V.B) >> [parent(V.X, V.A), sibling(V.Y, V.X), parent(V.Y, V.B)]

# +collatz(V.N, V.N)
# collatz(V.N0, V.N) >> [equals(0, V.N0 % 2), equals(V.N1, V.N0 / 2), collatz(V.N1, V.N)]
# collatz(V.N0, V.N) >> [equals(1, V.N0 % 2), equals(V.N1, 3 * V.N0 + 1), collatz(V.N1, V.N)]

# inboth(V.A, V.B, V.X) >> [member(V.X, V.A), member(V.X, V.B)]

+just_ate(C.deer, C.grass)
+just_ate(C.tiger, C.deer)

is_digesting(V.A, V.B) >> [just_ate(V.A, V.B)]
is_digesting(V.A, V.B) >> [just_ate(V.A, V.C), is_digesting(V.C, V.B)]

# +count(V.A, V.A)
# count(V.A, V.C) >> [equals(V.B, V.A + 1), count(V.B, V.C)]

+always_true()

# increment_all([], V.X) >> [setEqual(V.X, [])]
# increment_all([V.H, "|", V.T], V.X) >> [equals(V.Y, V.H + 1), increment_all(V.T, V.Z), setEqual(V.X, [V.Y, "|", V.Z])]

# +basicList([C.a, C.b, C.c])

# +merge("A, [], "A)
# +merge([], "B, "B)
# merge(["H1, "|, "T1"], ["H2, "|, "T2"], "X) >> ["H1 < H2, merge("T1, ["H2, "|, "T2"], "Z), setEqual("X, ["H1, "|, "Z"])]
# merge(["H1, "|, "T1"], ["H2, "|, "T2"], "X) >> ["H1 >= H2, merge(["H1, "|, "T1"], "T2, "Z), setEqual("X, ["H2, "|, "Z"])]

# ##########################################

# ### All tests below succeed! ###

success = -male(V.X)
success = -child(C.bob, V.X)
success = -child(V.X, C.bob)
success = -child(V.X, C.john)
success = -child(C.rosa, C.isidore)
success = -parent(C.rosa, C.kathryn)
# success = -parent("rosa, "X)
# success = -father("john, "X)
# success = -mother("rosa, "X)
# success = -mother("john, "X)
# success = -mother("X, "john)
# success = -ancestor("X, "bob)
# success = -ancestor("ben, "X)
# success = -collatz("10, "X)
# success = -member("X, ["bob, "apple, "shirt, "pip"])
# success = -inboth(["green, "red, "orange"], ["apple, "orange, "pear"], "orange)
# success = -inboth(["1, "2, "3, "4"], ["2, "5, "6, "1"], "X)
# success = -write("hi)
# success = -equals("X, "2 + 4)
# success = -equals("6, "2 + 4)
# success = -equals("6, "2 + 8)
# success = -equals("X, "2 + hi)    # Maybe print error instead???
# success = -fail()
# success = -is_digesting("tiger, "grass)
# success = -count(0, V.X)
# success = -always_true()
# success = -setEqual("X, [])
# success = -increment_all(["12, "99, "4, "-7"], "X)
# success = -basicList(["X, "Y, "Z"])



### Testing Zone ###








#### Test queries below FAIL ####  ???

# success = -sibling("john, "X)
# success = -first_cousin("david, "X)
# success = -first_cousin("jiri, "X)
# success = -merge(["1, "4, "5, "10, "11, "13"], ["3, "4, "1000"], "X)
# child(X, emma), male(X).
# success = -(child("X, "emma) & male("X))   <- ugly, but maybe this???
# child(alice, rosa), female(alice).











### To see all results #####
for s in success:   # Can also be '-success' to reduce typing '-' elsewhere.
    print(s)

# #### Alternatives for specific cases ####
# for s in -male("X):
#     print(s)

# print(next(success))
# print(next(success))

# ### To see only some results ####
# for _ in range(5):
#     print(next(success))



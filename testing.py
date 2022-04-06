# This file is used for internal testing.
from PL import *
# from Experimenting import *


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
ismember = Predicate("ismember")
ismember2 = Predicate("ismember2")
all_diff = Predicate("all_diff")
splitAt = Predicate("splitAt")
someTree = Predicate("someTree")
sublist = Predicate("sublist")
sublist_cut = Predicate("sublist_cut")
isSorted = Predicate("isSorted")
bad_sort = Predicate("bad_sort")
teaches = Predicate("teaches")
studies = Predicate("studies")

# #### facts/rules ####

+male("bob")
+male("john")
+male("ben")
+male("martin")
+male("edmund")
+male("david")
+male("isidore")
+male("william")
+male("ferdinand")
+male("morris")
+male("alphonse")
+male("jiri")
+female("kathryn")
+female("beatrice")
+female("rachel")
+female("lillian")
+female("alice")
+female("rosa")
+female("marjorie")
+female("emma")
+female("nellie")
+female("eva")
+female("bertha")
+female("fergie")

# A is the child of B
+child("bob", "john")
+child("bob", "kathryn")
+child("beatrice", "john")
+child("beatrice", "kathryn")
+child("john", "ben")
+child("john", "rachel")
+child("lillian", "ben")
+child("lillian", "rachel")
+child("kathryn", "rosa")
+child("kathryn", "martin")
+child("alice", "martin")
+child("alice", "rosa")
+child("ferdinand", "martin")
+child("ferdinand", "fergie")
+child("marjorie", "edmund")
+child("marjorie", "lillian")
+child("david", "lillian")
+child("david", "edmund")
+child("ben", "isidore")
+child("ben", "bertha")
+child("william", "isidore")
+child("william", "bertha")
+child("emma", "isidore")
+child("emma", "bertha")
+child("morris", "alphonse")
+child("morris", "emma")
+child("nellie", "alphonse")
+child("nellie", "emma")
+child("eva", "alphonse")
+child("eva", "emma")
+child("jiri", "alphonse")
+child("jiri", "emma")

parent("A", "B") >> [child("B", "A")]

father("A", "B") >> [male("A"), parent("A", "B")]
mother("A", "B") >> [female("A"), parent("A", "B")]

sibling("A", "B") >> [parent("X", "A"), parent("X", "B"), notEqual("A", "B")]

uncle("A", "B") >> [parent("X", "B"), sibling("A", "X"), male("A")]
aunt("A", "B") >> [parent("X", "B"), sibling("A", "X"), female("A")]

ancestor("A", "B") >> [parent("A", "B")]
ancestor("A", "B") >> [parent("A", "X"), ancestor("X", "B")]

first_cousin("A", "B") >> [parent("X", "A"), sibling("Y", "X"), parent("Y", "B")]

+collatz("N", "N")
collatz("N0", "N") >> [is_(0, "N0" |mod| 2), is_("N1", "N0" |div| 2), collatz("N1", "N")]
collatz("N0", "N") >> [is_(1, "N0" |mod| 2), is_("N1", 3 |times| "N0" |plus| 1), collatz("N1", "N")]

inboth("A", "B", "X") >> [member("X", "A"), member("X", "B")]

+just_ate("deer", "grass")
+just_ate("tiger", "deer")

is_digesting("A", "B") >> [just_ate("A", "B")]
is_digesting("A", "B") >> [just_ate("A", "C"), is_digesting("C", "B")]

+count("A", "A")
count("A", "C") >> [is_("B", "A" |plus| 1), count("B", "C")]

+always_true()

increment_all([], "X") >> [setEqual("X", [])]
increment_all(["H", "|", "T"], "X") >> [is_("Y", "H" |plus| 1), increment_all("T", "Z"), setEqual("X", ["Y", "|", "Z"])]

# increment_all([], "X") >> [setEqual("X", [])]
# increment_all(["H", Tail("T")], "X") >> [is_("Y", "H" |plus| 1), increment_all("T", "Z"), setEqual("X", ["Y", Tail("Z")])]

+basicList(["a", "b", "c"])

+merge("A", [], "A")
+merge([], "B", "B")
merge(["H1", "|", "T1"], ["H2", "|", "T2"], "X") >> [lt_("H1", "H2"), merge("T1", ["H2", "|", "T2"], "Z"), setEqual("X", ["H1", "|", "Z"])]
merge(["H1", "|", "T1"], ["H2", "|", "T2"], "X") >> [ge_("H1", "H2"), merge(["H1", "|", "T1"], "T2", "Z"), setEqual("X", ["H2", "|", "Z"])]

+ismember("H", ["H", "|", "_"]) 
ismember("H", ["_", "|", "T"]) >> [ismember("H", "T")]

ismember2("H", ["H", "|", "_"]) >> [cut()]
ismember2("H", ["_", "|", "T"]) >> [ismember2("H", "T")]

all_diff([]) >> []
all_diff(["H", "|", "T"]) >> [not_(member("H", "T")), all_diff("T")]    # Problem is member args are never created. ???

splitAt("Pos", "List", "FirstPart", "SecondPart") >> [append_("FirstPart", "SecondPart", "List"), len_("FirstPart", "Pos")]

sublist("A", "B") >> [append_("A", "_", "B")]
sublist("A", ["_", "|", "T"]) >> [sublist("A", "T")]

# sublist_cut(A, B) :- append(A, _, B), !.
# sublist_cut(A, [_|T]) :- sublist_cut(A, T).
sublist_cut("A", "B") >> [append_("A", "_", "B"), cut()]
sublist_cut("A", ["_", "|", "T"]) >> [sublist_cut("A", "T")]

# isSorted([_]).
# isSorted([H1, H2 | T]) :- H1 =< H2, isSorted([H2 | T]).
+isSorted(["_"])
isSorted(["H1", "H2", "|", "T"]) >> [le_("H1", "H2"), isSorted(["H2", "|", "T"])]


# bad_sort(X, Y) :- permutation(X, Y), isSorted(Y), !.
bad_sort("X", "Y") >> [permutation_("X", "Y"), isSorted("Y"), cut()]


# teaches(dr_fred, history).
teaches("dr_fred", "history") >> []
# teaches(dr_fred, english).
teaches("dr_fred", "english") >> []
# teaches(dr_fred, drama).
teaches("dr_fred", "drama") >> []
# teaches(dr_fiona, physics).
teaches("dr_fiona", "physics") >> []         	
# studies(alice, english).
studies("alice", "english") >> []
# studies(angus, english).
studies("angus", "english") >> []
# studies(amelia, drama).
studies("amelia", "drama") >> []
# studies(alex, physics).
studies("alex", "physics") >> []

# ##########################################

# ### All tests below succeed! ###

# query << [male("X")]
# query << [child("bob", "X")]
# query << [child("X", "Y")]
# query << [child("X", "bob")]
# query << [child("X", "john")]
# query << [child("X", "emma"), male("X")]
# query << [child("alice", "rosa"), female("alice")]
# query << [child("rosa", "isidore")]
# query << [parent("rosa", "kathryn")]
# query << [parent("rosa", "X")]
# query << [father("john", "X")]
# query << [mother("rosa", "X")]
# query << [mother("john", "X")]
# query << [mother("X", "john")]
# query << [sibling("john", "X")]
# query << [sibling("X", "ben")]
# query << [sibling("ferdinand", "alice")]
# query << [aunt("X", "john")]
# query << [uncle("X", "john")]
# query << [uncle("william", "X")]
# query << [ancestor("X", "bob")]
# query << [ancestor("ben", "X")]
# query << [first_cousin("david", "X")]
# query << [first_cousin("jiri", "X")]
# query(9) << [collatz(10, "X")]          # To see only some results, use query(number_of_results).
# query << [member("X", ["bob", "apple", "shirt", "pip"])]
# query << [inboth(["green", "red", "orange"], ["apple", "orange", "pear"], "orange")]
# query << [inboth([1, 2, 3, 4], [2, 5, 6, 1], "X")]
# query << [increment_all([12, 99, 4, -7], "X")]
# query << [merge([1, 4, 5, 10, 11, 13], [3, 4, 1000], "X")]
# query << [all_diff(["a", "b", "c"])]
# query << [all_diff(["a", "b", "c", "b"])]
# query << [between(1, 3, "X"), between(1, 3, "Y"), between(1, 3, "Z"), all_diff(["X", "Y", "Z"])]
# query << [not_(member("X", ["a", "b", "c"])), setEqual("X", "f")]
# query << [setEqual("X", ["q", "y", "z", "w"]), not_(len_("X", 4))]
# query << [setEqual("X", 3 |plus| 4), not_(setEqual("X", 99))]
# query << [setEqual("X", "f"), not_(member("X", ["a", "b", "c"]))]
# query << [write("hi")]
# query << [is_("X", 2 |plus| 4)]
# query << [is_(6, 2 |plus| 4)]
# query << [is_(6, 2 |plus| 8)]           # Results don't show false if previous query was true. Good or bad?
# query << [is_("X", 2 |plus| "hi")]    # Change error later. ???
# query << [fail()]
# query << [is_digesting("tiger", "grass")]
# query << [is_digesting("X", "Y")]
# query(10) << [count(0, "X")]
# query << [always_true()]
# query << [setEqual("X", [])]
# query << [basicList(["X", "Y", "Z"])]
# query << [is_("X", 2 |plus| (4 |times| 5))]
# query << [is_("X", 2 |plus| 4 |times| 5)]
# query << [is_("X", 2 |times| 4 |plus| 5)]
# query << [is_("X", 2 |times| 4 |times| 5 |plus| 2)]
# query << [is_("X", 4 |minus| 3)]
# query << [is_(4, 2 |plus| "X" |plus| 5)]     # is_ pred can't have vars on right side.
# query << [append_([1, 2, 3], ["a", "b"], "X")]
# query << [append_("A", "B", [1, 2, 3, 4, 5])]
# query << [ismember(1, [1, 2, 3, 1])]
# query << [between(1, 5, "K")]
# query << [lt_(1, 1 |plus| 2)]
# query << [lt_(1 |plus| 2, 1)]
# query << [splitAt(3, ["a", "b", "c", "d", "e", "f", "g", "h"], "A", "B")]
# query << [sublist(["a", "a"], ["b", "a", "a", "b"])]
# query << [sublist(["b", "a", "b"], ["b", "a", "a", "b"])]
# query << [sublist(["a", "b", "a"], ["b", "a", "a", "b"])]
# query << [sublist(["a"], ["b", "a", "a", "b"])]
# query << [sublist(["a", "b", "d"], ["a", "b", "c", "d"])]
# query << [member("X", [4, 5, 14, 15, 24, 25]), gt_("X", 10), cut(), is_(0, "X" |mod| 2)]
# query << [member("X", [4, 5, 14, 15, 24, 25]), gt_("X", 10), is_(0, "X" |mod| 2)]
# query << [member("X", [4, 5, 14, 15, 24, 25]), cut(), gt_("X", 10), is_(0, "X" |mod| 2)]
# query << [member("X", [3, 4, 5, 13, 14, 15, 23, 24, 25]), gt_("X", 10), cut(), is_(0, "X" |mod| 2)]
# query << [isSorted([1, 2])]
# query << [isSorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]
# query << [isSorted([1, 2, 3, 4, 10, 6, 7, 8, 9, 10])]
# query << [permutation_([1, 2, 3], "X")]
# query << [permutation_([1, 2], [2, 1])]
# query << [permutation_([1, 2, 3], [2, 3, 1])]


### Testing Zone ###

# query << [bad_sort([5, 3, 1, 10, 3], "Y")]
query << [ismember2(1, [1, 2, 3, 1])]
# query << [ismember2("X", [1, 2, 3, 1])]
# query << [sublist_cut(["a"], ["b", "a", "a", "b"])]
# query << [teaches("dr_fred", "Course"), studies("Student", "Course")]
# query << [teaches("dr_fred", "Course"), cut(), studies("Student", "Course")]
# query << [teaches("dr_fred", "Course"), studies("Student", "Course"), cut()]
# query << [cut(), teaches("dr_fred", "Course"), studies("Student", "Course")]


#### Test queries below FAIL ####  ???





# query << [between(1, 5, "X"), mynot(setEqual("X", 3))]  # Fails because my predicates can't take other predicates as args.


### To see results ###
for s in query:   # Can also be '-success' to reduce typing '-' elsewhere.
    print(s)
    # # If you want to use the results, you can do something like this:
    # X = s["B"]
    # print(X)

# The query can be indexed to find a specific result.
# print(query[5])




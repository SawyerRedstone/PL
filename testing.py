# This file is used for internal testing.
# from PL import *
import PL
# from maze import *
# from primeFactors import *
# from Experimenting import *


################### Testing #####################

# First we define all the predicates that will be tested.
male = PL.Predicate("male")
female = PL.Predicate("female")
child = PL.Predicate("child")
parent = PL.Predicate("parent")
father = PL.Predicate("father")
mother = PL.Predicate("mother")
sibling = PL.Predicate("sibling")
uncle = PL.Predicate("uncle")
aunt = PL.Predicate("aunt")
ancestor = PL.Predicate("ancestor")
first_cousin = PL.Predicate("first_cousin")
collatz = PL.Predicate("collatz")
inboth = PL.Predicate("inboth")
increment_all = PL.Predicate("increment_all")
just_ate = PL.Predicate("just_ate")
is_digesting = PL.Predicate("is_digesting")
count = PL.Predicate("count")
always_true = PL.Predicate("always_true")
basicList = PL.Predicate("basicList")
merge = PL.Predicate("merge")
ismember2 = PL.Predicate("ismember2")
all_diff = PL.Predicate("all_diff")
splitAt = PL.Predicate("splitAt")
someTree = PL.Predicate("someTree")
sublist = PL.Predicate("sublist")
sublist_cut = PL.Predicate("sublist_cut")
isSorted = PL.Predicate("isSorted")
bad_sort = PL.Predicate("bad_sort")
teaches = PL.Predicate("teaches")
studies = PL.Predicate("studies")
lookup = PL.Predicate("lookup")
graph1 = PL.Predicate("graph1")
graph2 = PL.Predicate("graph2")
graph3 = PL.Predicate("graph3")
hasCycle = PL.Predicate("hasCycle")
getChain = PL.Predicate("getChain")

# #### facts/rules ####

male("bob") >> []
male("john") >> []
male("ben") >> []
male("martin") >> []
male("edmund") >> []
male("david") >> []
male("isidore") >> []
male("william") >> []
male("ferdinand") >> []
male("morris") >> []
male("alphonse") >> []
male("jiri") >> []
female("kathryn") >> []
female("beatrice") >> []
female("rachel") >> []
female("lillian") >> []
female("alice") >> []
female("rosa") >> []
female("marjorie") >> []
female("emma") >> []
female("nellie") >> []
female("eva") >> []
female("bertha") >> []
female("fergie") >> []

# A is the child of B
child("bob", "john") >> []
child("bob", "kathryn") >> []
child("beatrice", "john") >> []
child("beatrice", "kathryn") >> []
child("john", "ben") >> []
child("john", "rachel") >> []
child("lillian", "ben") >> []
child("lillian", "rachel") >> []
child("kathryn", "rosa") >> []
child("kathryn", "martin") >> []
child("alice", "martin") >> []
child("alice", "rosa") >> []
child("ferdinand", "martin") >> []
child("ferdinand", "fergie") >> []
child("marjorie", "edmund") >> []
child("marjorie", "lillian") >> []
child("david", "lillian") >> []
child("david", "edmund") >> []
child("ben", "isidore") >> []
child("ben", "bertha") >> []
child("william", "isidore") >> []
child("william", "bertha") >> []
child("emma", "isidore") >> []
child("emma", "bertha") >> []
child("morris", "alphonse") >> []
child("morris", "emma") >> []
child("nellie", "alphonse") >> []
child("nellie", "emma") >> []
child("eva", "alphonse") >> []
child("eva", "emma") >> []
child("jiri", "alphonse") >> []
child("jiri", "emma") >> []

parent("A", "B") >> [child("B", "A")]

father("A", "B") >> [male("A"), parent("A", "B")]
mother("A", "B") >> [female("A"), parent("A", "B")]

sibling("A", "B") >> [parent("X", "A"), parent("X", "B"), PL.notEqual("A", "B")]

uncle("A", "B") >> [parent("X", "B"), sibling("A", "X"), male("A")]
aunt("A", "B") >> [parent("X", "B"), sibling("A", "X"), female("A")]

ancestor("A", "B") >> [parent("A", "B")]
ancestor("A", "B") >> [parent("A", "X"), ancestor("X", "B")]

first_cousin("A", "B") >> [parent("X", "A"), sibling("Y", "X"), parent("Y", "B")]

collatz("N", "N") >> []
collatz("N0", "N") >> [PL.is_(0, "N0" |PL.mod| 2), PL.is_("N1", "N0" |PL.div| 2), collatz("N1", "N")]
collatz("N0", "N") >> [PL.is_(1, "N0" |PL.mod| 2), PL.is_("N1", 3 |PL.times| "N0" |PL.plus| 1), collatz("N1", "N")]

inboth("A", "B", "X") >> [PL.member_("X", "A"), PL.member_("X", "B")]

just_ate("deer", "grass") >> []
just_ate("tiger", "deer") >> []

is_digesting("A", "B") >> [just_ate("A", "B")]
is_digesting("A", "B") >> [just_ate("A", "C"), is_digesting("C", "B")]

count("A", "A") >> []
count("A", "C") >> [PL.is_("B", "A" |PL.plus| 1), count("B", "C")]

always_true() >> []

increment_all([], "X") >> [PL.setEqual("X", [])]
increment_all(["H", "|", "T"], "X") >> [PL.is_("Y", "H" |PL.plus| 1), increment_all("T", "Z"), PL.setEqual("X", ["Y", "|", "Z"])]

basicList(["a", "b", "c"]) >> []

merge("A", [], "A") >> []
merge([], "B", "B") >> []
merge(["H1", "|", "T1"], ["H2", "|", "T2"], "X") >> [PL.lt_("H1", "H2"), merge("T1", ["H2", "|", "T2"], "Z"), PL.setEqual("X", ["H1", "|", "Z"])]
merge(["H1", "|", "T1"], ["H2", "|", "T2"], "X") >> [PL.ge_("H1", "H2"), merge(["H1", "|", "T1"], "T2", "Z"), PL.setEqual("X", ["H2", "|", "Z"])]

ismember2("H", ["H", "|", "_"]) >> [PL.cut()]
ismember2("H", ["_", "|", "T"]) >> [ismember2("H", "T")]

all_diff([]) >> []
all_diff(["H", "|", "T"]) >> [PL.not_(PL.member_("H", "T")), all_diff("T")]    # Problem is member args are never created. ???

splitAt("Pos", "List", "FirstPart", "SecondPart") >> [PL.append_("FirstPart", "SecondPart", "List"), PL.len_("FirstPart", "Pos")]

sublist("A", "B") >> [PL.append_("A", "_", "B")]
sublist("A", ["_", "|", "T"]) >> [sublist("A", "T")]

sublist_cut("A", "B") >> [PL.append_("A", "_", "B"), PL.cut()]
sublist_cut("A", ["_", "|", "T"]) >> [sublist_cut("A", "T")]

isSorted(["_"]) >> []
isSorted(["H1", "H2", "|", "T"]) >> [PL.le_("H1", "H2"), isSorted(["H2", "|", "T"])]

bad_sort("X", "Y") >> [PL.permutation_("X", "Y"), isSorted("Y"), PL.cut()]


teaches("dr_fred", "history") >> []
teaches("dr_fred", "english") >> []
teaches("dr_fred", "drama") >> []
teaches("dr_fiona", "physics") >> []         	
studies("alice", "english") >> []
studies("angus", "english") >> []
studies("amelia", "drama") >> []
studies("alex", "physics") >> []

lookup("K", "L", "V") >> [PL.member_("K-V", "L"), PL.cut()]

graph1(["n1-n2", "n2-n5", "n1-n3", "n1-n4", "n4-n6", "n6-n7", "n6-n8"]) >> []
graph2(["n1-n2", "n2-n5", "n1-n3", "n1-n4", "n4-n6", "n6-n7", "n7-n1", "n7-n8"]) >> []
graph3(["n4-n5", "n1-n2", "n1-n3", "n1-n4", "n4-n9", "n9-10", "n9-n11", "n9-n12", "n12-n9"]) >> []

hasCycle("G") >> [PL.member_("X-Y", "G"), getChain(["X"], "Y", "G"), PL.cut()]

getChain("Reached", "Next", "_G") >> [PL.member_("Next", "Reached"), PL.cut()]
getChain("Reached", "Next", "G") >> [PL.member_("Next-X", "G"), PL.append_("Reached", ["Next"], "NewReached"), getChain("NewReached", "X", "G"), PL.cut()]

# ##########################################

# ### All tests below succeed! ###

# PL.query << [male("X")]
# PL.query << [child("bob", "X")]
# PL.query << [child("X", "Y")]
# PL.query << [child("X", "bob")]
# PL.query << [child("X", "john")]
# PL.query << [child("X", "emma"), male("X")]
# PL.query << [child("alice", "rosa"), female("alice")]
# PL.query << [child("rosa", "isidore")]
# PL.query << [parent("rosa", "kathryn")]
# PL.query << [parent("rosa", "X")]
# PL.query << [father("john", "X")]
# PL.query << [mother("rosa", "X")]
# PL.query << [mother("john", "X")]
# PL.query << [mother("X", "john")]
# PL.query << [sibling("john", "X")]
# PL.query << [sibling("X", "ben")]
# PL.query << [sibling("ferdinand", "alice")]
# PL.query << [aunt("X", "john")]
# PL.query << [uncle("X", "john")]
# PL.query << [uncle("william", "X")]
# PL.query << [ancestor("X", "bob")]
# PL.query << [ancestor("ben", "X")]
# PL.query << [first_cousin("david", "X")]
# PL.query << [first_cousin("jiri", "X")]
# PL.query(9) << [collatz(10, "X")]          # To see only some results, use PL.query(number_of_results).
# PL.query << [PL.member_("X", ["bob", "apple", "shirt", "pip"])]
# PL.query << [inboth(["green", "red", "orange"], ["apple", "orange", "pear"], "orange")]
# PL.query << [inboth([1, 2, 3, 4], [2, 5, 6, 1], "X")]
# PL.query << [increment_all([12, 99, 4, -7], "X")]
# PL.query << [merge([1, 4, 5, 10, 11, 13], [3, 4, 1000], "X")]
# PL.query << [all_diff(["a", "b", "c"])]
# PL.query << [all_diff(["a", "b", "c", "b"])]
# PL.query << [PL.between(1, 3, "X"), PL.between(1, 3, "Y"), PL.between(1, 3, "Z"), all_diff(["X", "Y", "Z"])]
# PL.query << [PL.not_(PL.member_("X", ["a", "b", "c"])), PL.setEqual("X", "f")]
# PL.query << [PL.setEqual("X", "f"), PL.not_(PL.member_("X", ["a", "b", "c"]))]
# PL.query << [PL.setEqual("X", ["q", "y", "z", "w"]), PL.not_(PL.len_("X", 4))]
# PL.query << [PL.setEqual("X", 3 |PL.plus| 4), PL.not_(PL.setEqual("X", 99))]
# PL.query << [PL.write_("hi")]
# PL.query << [PL.is_("X", 2 |PL.plus| 4)]
# PL.query << [PL.is_(6, 2 |PL.plus| 4)]
# PL.query << [PL.is_(6, 2 |PL.plus| 8)]           # Results don't show false if previous PL.query was true. Good or bad?
# PL.query << [PL.is_("X", 2 |PL.plus| "hi")]    # Change error later. ???
# PL.query << [PL.fail_()]
# PL.query << [is_digesting("tiger", "grass")]
# PL.query << [is_digesting("X", "Y")]
# PL.query(10) << [count(0, "X")]
# PL.query << [always_true()]
# PL.query << [PL.setEqual("X", [])]
# PL.query << [basicList(["X", "Y", "Z"])]
# PL.query << [PL.is_("X", 2 |PL.plus| (4 |PL.times| 5))]
# PL.query << [PL.is_("X", 2 |PL.plus| 4 |PL.times| 5)]
# PL.query << [PL.is_("X", 2 |PL.times| 4 |PL.plus| 5)]
# PL.query << [PL.is_("X", 2 |PL.times| 4 |PL.times| 5 |PL.plus| 2)]
# PL.query << [PL.is_("X", 4 |PL.minus| 3)]
# PL.query << [PL.is_(4, 2 |PL.plus| "X" |PL.plus| 5)]     # is_ pred can't have vars on right side.
# PL.query << [PL.append_([1, 2, 3], ["a", "b"], "X")]
# PL.query << [PL.append_("A", "B", [1, 2, 3, 4, 5])]
# PL.query << [PL.member_(1, [1, 2, 3, 1])]
# PL.query << [PL.between(1, 5, "K")]
# PL.query << [PL.lt_(1, 1 |PL.plus| 2)]
# PL.query << [PL.lt_(1 |PL.plus| 2, 1)]
# PL.query << [splitAt(3, ["a", "b", "c", "d", "e", "f", "g", "h"], "A", "B")]
# PL.query << [sublist(["a", "a"], ["b", "a", "a", "b"])]
# PL.query << [sublist(["b", "a", "b"], ["b", "a", "a", "b"])]
# PL.query << [sublist(["a", "b", "a"], ["b", "a", "a", "b"])]
# PL.query << [sublist(["a"], ["b", "a", "a", "b"])]
# PL.query << [sublist(["a", "b", "d"], ["a", "b", "c", "d"])]
# PL.query << [PL.member_("X", [4, 5, 14, 15, 24, 25]), PL.gt_("X", 10), PL.cut(), PL.is_(0, "X" |PL.mod| 2)]
# PL.query << [PL.member_("X", [4, 5, 14, 15, 24, 25]), PL.gt_("X", 10), PL.is_(0, "X" |PL.mod| 2)]
# PL.query << [PL.member_("X", [4, 5, 14, 15, 24, 25]), PL.cut(), PL.gt_("X", 10), PL.is_(0, "X" |PL.mod| 2)]
# PL.query << [PL.member_("X", [3, 4, 5, 13, 14, 15, 23, 24, 25]), PL.gt_("X", 10), PL.cut(), PL.is_(0, "X" |PL.mod| 2)]
# PL.query << [isSorted([1, 2])]
# PL.query << [isSorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]
# PL.query << [isSorted([1, 2, 3, 4, 10, 6, 7, 8, 9, 10])]
# PL.query << [PL.permutation_([1, 2, 3], "X")]
# PL.query << [PL.permutation_([1, 2], [2, 1])]
# PL.query << [PL.permutation_([1, 2, 3], [2, 3, 1])]
# PL.query << [bad_sort([5, 3, 1, 10, 3], "Y")]
# PL.query << [ismember2(1, [1, 2, 3, 1])]
# PL.query << [ismember2("X", [1, 2, 3, 1])]
# PL.query << [sublist_cut(["a"], ["b", "a", "a", "b"])]
# PL.query << [teaches("dr_fred", "Course"), studies("Student", "Course")]
# PL.query << [teaches("dr_fred", "Course"), PL.cut(), studies("Student", "Course")]
# PL.query << [teaches("dr_fred", "Course"), studies("Student", "Course"), PL.cut()]
# PL.query << [PL.cut(), teaches("dr_fred", "Course"), studies("Student", "Course")]
# PL.query << [newPos(11, 1, "n", "NewR", "NewC")]
# PL.query << [newPos(11, 1, "w", "NewR", "NewC")]
# PL.query << [newPos(11, 1, "e", "NewR", "NewC")]
# PL.query << [newPos(11, 1, "s", "NewR", "NewC")]
# PL.query << [move(11, 1, "NewR", "NewC", [[11, 2]], "Visited", ["w", "w", "w"], "Dirs")]
# PL.query << [PL.reverse_([1,2,3], "X")]
# PL.query << [printUnsolvedMaze()]
# PL.query << [prime_factors(12, "X")]     # Maybe use for demonstration. ***
# PL.query << [PL.not_(male("bob"))]
# PL.query << [printSolvedMaze()]
# PL.query << [PL.between(1, 5, "X"), PL.not_(PL.setEqual("X", 3))]


### Testing Zone ###

#### Test queries below FAIL ####  ???


# PL.query << [lookup(5, ["6-a", "7-z", "5-t", "34-w"], "Value")]
# PL.query << [lookup("Key", ["6-a", "7-z", "5-t", "34-w"], "z")]
# PL.query << [lookup(6, ["6-a", "7-z", "5-t", "34-w", "6-foo"], "Value")]
# PL.query << [graph2("G"), hasCycle("G")]

### To see results ###
for result in PL.query:
    print(result)
    # # If you want to use the results, you can do something like this:
    # X = result["X"]
    # print(X)

# The query can be indexed to find a specific result.
# print(PL.query[2])

PL.beginQuerying()


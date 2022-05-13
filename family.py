from PL import *

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

sibling("A", "B") >> [parent("X", "A"), parent("X", "B"), notEqual("A", "B")]

uncle("A", "B") >> [parent("X", "B"), sibling("A", "X"), male("A")]
aunt("A", "B") >> [parent("X", "B"), sibling("A", "X"), female("A")]

ancestor("A", "B") >> [parent("A", "B")]
ancestor("A", "B") >> [parent("A", "X"), ancestor("X", "B")]

first_cousin("A", "B") >> [parent("X", "A"), sibling("Y", "X"), parent("Y", "B")]

######################################
# Examples below. Uncomment to test. #
######################################

# query << [male("X")]
# query << [child("X", "emma"), male("X")]    # Compound query.
# query << [parent("rosa", "kathryn")]
# query << [father("john", "X")]
# query << [ancestor("X", "bob")]

# print(query)

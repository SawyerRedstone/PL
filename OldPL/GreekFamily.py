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

# Add facts of the male Greek gods.
# These facts are written in the form male(name) >> [].
male("zeus") >> []
male("atlas") >> []
male("apollo") >> []
male("eros") >> []
male("dionysus") >> []
male("kratos") >> []
male("morpheus") >> []
male("hermes") >> []
male("ares") >> []
male("charon") >> []
male("pan") >> []
male("zephyrus") >> []
male("cronus") >> []
male("erebus") >> []
male("asclepius") >> []


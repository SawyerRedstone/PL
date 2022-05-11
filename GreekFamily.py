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

male("zeus") >> []
female("hera") >> []

# Check to see if any names aren't mentioned in genders. ***
child("hercules", "zeus") >> []
child("athena", "zeus") >> []
child("ares", "hera") >> []
child("eileithyia", "hera") >> []
child("hebe", "hera") >> []
child("hephaestus", "hera") >> []
# Determine the prime factors of a given positive integer.
 
from PL import *
 
prime_factors = Predicate("prime_factors")
next_factor = Predicate("next_factor")
 
prime_factors("N", "L") >> [gt_("N", 0), prime_factors("N", "L", 2)]
prime_factors(1, [], "_") >> [cut()]
prime_factors("N", ["F", "|", "L"], "F") >> [
    is_("R", "N // F"),
    is_("N", "R * F"),
    cut(), prime_factors("R", "L", "F")]
prime_factors("N", "L", "F") >> [next_factor("N", "F", "NF"), prime_factors("N", "L", "NF")]
 
next_factor("_", "2", "3") >> [cut()]
next_factor("N", "F", "NF") >> [
    lt_("F * F", "N"), cut(),
    is_("NF", "F + 2")]
next_factor("N", "_", "N") >> []
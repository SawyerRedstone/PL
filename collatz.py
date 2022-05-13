from PL import *

collatz = Predicate("collatz")

collatz("N", "N") >> []
collatz("N0", "N") >> [
    equals(0, "N0 % 2"), 
    equals("N1", "N0 / 2"), 
    collatz("N1", "N")]
collatz("N0", "N") >> [
    equals(1, "N0 % 2"), 
    equals("N1", "3 * N0 + 1"), 
    collatz("N1", "N")]

######################################
# Examples below. Uncomment to test. #
######################################

# # This predicate has infinite results, so queries must be limited to fewer results.

# query(3) << [collatz(10, "L")]      # Query for 3 results.	
# print(query)                        # prints [{'L': '10'}, {'L': '5.0'}, {'L': '16.0'}]

# query(4) << [collatz(8, "L")]       # Query for 4 results.	
# print(query)                        # prints [{'L': '8'}, {'L': '4.0'}, {'L': '2.0'}, {'L': '1.0'}]
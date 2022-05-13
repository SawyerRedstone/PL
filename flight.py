from PL import *


# simple flight-planning system

airport = Predicate("airport")
flight = Predicate("flight")
flights = Predicate("flights")

# airport(City,Code)
# ------------------
# matches a city name with an airport code, e.g. "nanaimo" with "ycd"
airport("'Nanaimo'", "'YCD'") >> []
airport("'Vancouver'", "'YVR'") >> []
airport("'Victoria'", "'YYJ'") >> []
airport("'Calgary'", "'YYC'") >> []
airport("'Lethbridge'", "'YQL'") >> []
airport("'Kamloops'", "'YKA'") >> []


# flight(DeptAC, ArrAC)
# ---------------------
# as a fact, states there is a direct flight between the
#    departure airport and arrival airport,
# under the given flight code (e.g. "AC123")
flight("'YCD'", "'YYC'") >> []
flight("'YCD'", "'YVR'") >> []
flight("'YKA'", "'YQL'") >> []
flight("'YKA'", "'YYC'") >> []
flight("'YQL'", "'YKA'") >> []
flight("'YQL'", "'YVR'") >> []
flight("'YQL'", "'YYC'") >> []
flight("'YYJ'", "'YVR'") >> []
flight("'YYJ'", "'YYC'") >> []
flight("'YVR'", "'YYC'") >> []
flight("'YVR'", "'YQL'") >> []
flight("'YVR'", "'YCD'") >> []
flight("'YVR'", "'YYJ'") >> []
flight("'YYC'", "'YQL'") >> []
flight("'YYC'", "'YKA'") >> []
flight("'YYC'", "'YCD'") >> []
flight("'YYC'", "'YYJ'") >> []
flight("'YYC'", "'YVR'") >> []


# flights(DeptAC, ArrAC)
# ----------------------
# as a rule, finds a sequence (list) of flights connecting
#    the departure airport to the arrival airport

# direct flight
flights("D", "A") >> [
    airport("Dname", "D"), 
    airport("Aname", "A"), 
    flight("D", "A"), 
    format_("Direct flight {}({}) to {}({})\n", ["Dname", "D", "Aname", "A"])]


# one-stop
flights("D", "A") >> [
    flight("D", "I"), notEqual("I", "A"), flight("I", "A"), 
    airport("Dname", "D"), airport("Iname", "I"), airport("Aname", "A"),
    format_("Flight {}({}) to {}({}) via {}({})\n", ["Dname", "D", "Aname", "A", "Iname", "I"])]


# two-stop
flights("D", "A") >> [
    flight("D", "I"), notEqual("I", "A"), flight("I", "J"), notEqual("J", "A"),
    notEqual("J", "D"), flight("J", "A"), airport("Dname", "D"),
    airport("Aname", "A"), airport("Iname", "I"), airport("Jname", "J"),
    format_("Flight {}({}) to {}({}) via {}({}) and {}({})\n", ["Dname", "D", "Aname", "A", "Iname", "I", "Jname", "J"])]

# flights(DeptCity, ArrCity)
# --------------------------
# run a flights query, but starting with the city name (translate to airport codes)
flights("DC", "AC") >> [airport("DC", "D"), airport("AC", "A"), flights("D", "A")]

# Example query:
# query << [flights("'Nanaimo'", "'Calgary'")] 

# This query prints the following output:

# Direct flight Nanaimo(YCD) to Calgary(YYC)
# Flight Nanaimo(YCD) to Calgary(YYC) via Vancouver(YVR)
# Flight Nanaimo(YCD) to Calgary(YYC) via Vancouver(YVR) and Lethbridge(YQL)
# Flight Nanaimo(YCD) to Calgary(YYC) via Vancouver(YVR) and Victoria(YYJ)


# The PL Module offers Prolog functionality for Python programmers.
# Created by Sawyer Redstone.

import itertools

# Take a list, string, or int, and convert it to type Term.
def create(term, memo = {}):
    if str(term) in memo:
        return memo[str(term)]
    if isinstance(term, Goal):
        memo[str(term)] = Goal(term.pred, [create(arg, memo) for arg in term.args])
    if isinstance(term, int) or isinstance(term, float):   # Numbers are constants.
        memo[str(term)] = Const(term)
    elif isinstance(term, Math):
        # Make new math term so each alt has unchanged starting math.
        newMath = Math(term.function)
        newMath.mathList = [create(item, memo) if not callable(item) else item for item in term.mathList]
        memo[str(term)] = newMath
    elif isinstance(term, list):
        # If the list is empty, it is a Const; otherwise it is a ListPL.
        memo[str(term)] = ListPL([create(item, memo) for item in term]) if term else Const(term)
    elif isinstance(term, Goal):
        memo[str(term)] = Goal(term.pred, [create(item, memo) for item in term.args])
    # # If it has a dash, it must be a Pair.
    # elif "-" in term:       # ***
    #     term = term.replace(" ", "")    # Remove any extra spaces.
    #     term = term.split("-")          
    #     memo[str(term)] = Pair(create(term[0], memo), create(term[1], memo))
        # memo[str(term)] = Pair([create(item, memo) for item in pairList])
    elif term[0].isupper():
        memo[str(term)] = Var(term)
    elif term[0] == "_":        # Vars that start with "_" are temporary.
        return Var(term)        # Since all _s are different, they should not be added to memo.
    # Otherwise, it is a Const.
    else:
        # If the string is an int or float, convert it to the appropriate type.
        try:
            term = float(term)
            if term.is_integer():
                term = int(term)
        except ValueError:
            pass
        memo[str(term)] = Const(term)
    return memo[str(term)]


preds = {}      # Dict where key:var = name:predicate.


class Predicate():
    def __init__(self, name):
        preds[name] = self
        self.name = name            # The name of the predicate
        self.alternatives = {}      # Dict filled with all of the predicate alternatives, with arity as key.
    def __repr__(self):
        return self.name
    def __call__(self, *args):
        return Goal(self, args)

# Query is an iterator.
# Use query << [list of goals] for queries.
class Query():
    def __init__(self):
        self.goals = []
        self.successes = []
        self.size = None
    def __lshift__(self, goals):
        # Memo is a dictionary of all args in the goals.
        # This makes sure that no terms are duplicates.
        memo = {}
        goals = [Goal(goal.pred, [create(arg, memo) for arg in goal.args]) for goal in goals]
        attempt = tryGoals(goals)
        # Loop through the generator self.size times, or until end if size is not specified.
        for attempt in itertools.islice(attempt, self.size):
            success = attempt[0]
            wasCut = attempt[1]
            if not success:
                break
            args = {}
            for argName in memo:
                if isinstance(memo[argName], Var):
                    args[argName] = str(flatten(memo[argName].value))
            if len(args) > 0:
                # print("TEST: " + str(args))    # For debugging. ***
                self.successes.append(args)
            else:
                # print("TEST: True")    # For debugging. ***
                self.successes.append(True)
            if wasCut:
                break
        if self.successes == []:
            self.successes.append(False)
        # Reset the size for future queries, in the case where multiple queries are made at once.
        self.size = None
    def __iter__(self):
        return iter(self.successes)
    # query(3) makes the query only show 3 results.
    def __call__(self, num):
        self.size = num
        return self
    def __getitem__(self, num):
        return self.successes[num]


# Goals must be completed in order to satisfy a query.
class Goal():
    def __init__(self, pred = [], args = []):
        self.pred = pred            # The predicate that is being queried.
        self.args = list(args)      # Create a list of the goal's arguments.
        self.value = self           # This allows goals to unify with Vars.
    def __str__(self):
        return "goalPred: " + self.pred.name + "\nGoalArgs: " + str(self.args) + "\n"
    # Add facts as: head >> []
    # Add rules as: head >> [goal1, goal2, ...]
    def __rshift__(self, others):
        if len(self.args) in self.pred.alternatives:
            self.pred.alternatives[len(self.args)].append(Alt(self.pred, self.args, others))
        else:
            self.pred.alternatives[len(self.args)] = [Alt(self.pred, self.args, others)]
    def __repr__(self):
        return self.pred.name
    def unifyWith(self, other):
        if isinstance(other, Var):
            other.value = self
        return True



# Alts are individual alternatives that were added to a predicate.
class Alt():
    def __init__(self, pred, args, goals):
        self.pred = pred
        self.args = args
        self.goals = goals
    def __str__(self):
        # return "altArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
        return "alt from pred: " + self.pred.name + "\naltArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
    def __repr__(self):
        return "alt from pred: " + self.pred.name


# This function tries to unify the query and alt args, and returns a bool of its success.
def tryUnify(queryArgs, altArgs):
    for queryArg, altArg in zip(queryArgs, altArgs):    # Loop through the query and alt arguments.
        # Check if unification is possible before unifying.
        if queryArg != altArg:
            return False
        queryArg.unifyWith(altArg)
    return True                                 # If it reaches this point, they can be unified.


# Variables and Constants are Terms.
class Term():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []                  # The children are the variables that will change if this term has a value.
    @staticmethod
    def changeType(word):
        if isinstance(word, list):
            if word == []:
                return Const(word)
            elif word[0].value == "|":
                return word[-1]
            return ListPL(word)
        # All other values are Consts.
        return Const(word)
    # This checks if they *can* be equal.
    def __eq__(self, other):
        return self.value == other.value or not self or not other
    def __bool__(self):
        return self.value != "Undefined"    # A term is false it if has no value.
    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)
    def __hash__(self):
        return hash(repr(self))
    def unifyWith(self, altArg):
        altArg.children.append(self)                        # The children are the variables we want to find out.
        if self:
            altArg.value = self.value
        changePath(altArg, altArg.value)  # Set all unified terms to new value.
        return True


class Var(Term):
    def __init__(self, name, value = "Undefined"):
        self.name = name
        self.value = value
        super().__init__(name = self.name, value = self.value)    # Initialize the Var.
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))


class Const(Term):  # A constant, aka an atom.
    def __init__(self, value):
        super().__init__(name = "Const", value = value)


# To use math, write the operation surrounded with |.
# For example, '3 + 4' would be written as '3 |plus| 4'.
# (Idea from: https://code.activestate.com/recipes/384122/)
class Math(Term):
    def __init__(self, function):
        self.mathList = []
        self.function = function
        self.children = []     # The children are the variables that will change if this term has a value.
    def __ror__(self, other):
        # Make a new Math object so built-in objects won't change.
        newMath = Math(self.function)
        newMath.mathList = [other, self.function]
        return newMath
    def __or__(self, other):
        # Check if 'other' is built-in. (Add other built-in here! ***)
        if other is plus or other is minus:
            other = other.function
        if self.mathList[-1] is times or self.mathList[-1] is div or self.mathList[-1] is mod or self.mathList[-1] is floorDiv:
            op = self.mathList.pop()
            addend = self.mathList.pop()
            newMath = addend | op | other
            self.mathList.append(newMath)
        self.mathList.append(other)
        return self
    # This gives the object the .value attribute.
    @property
    def value(self):
        result = self.mathList[0].value
        for index, item in enumerate(self.mathList):
            if callable(item):
                addend = self.mathList[index+1].value
                result = item(result, addend)
        return result
    def __str__(self):
        return str(self.mathList)
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(tuple(self.mathList))


class ListPL(Term):
    def __init__(self, terms, name = "List"):
        self.head = terms[0]
        self.tail = Term.changeType(terms[1:])
        self.terms = terms      # The list of terms before they were seperated into a head and tail.
        super().__init__(name = name, value = terms)
    def __len__(self):
        return len(self.value)
    def __eq__(self, other):
        if isinstance(other.value, list) and other.value:       # ***
            other = ListPL(other.value)
        if self.tail and not isinstance(self.tail, ListPL):     # Should this be here or in different method? ***
            self.tail = Term.changeType(self.tail.value)
        if isinstance(other, ListPL):
            return self.head == other.head and self.tail == other.tail
        return super().__eq__(other)
    def unifyWith(self, altArg):
        if isinstance(altArg.value, list) and altArg.value:       # ***
            altArg = ListPL(altArg.value)
        if isinstance(altArg, ListPL):
            if self.head.unifyWith(altArg.head) and self.tail.unifyWith(altArg.tail):   # Later needs to clear path of all this? ***
                return True
            return False
        return super().unifyWith(altArg)
    def __str__(self):          # Maybe remove this? ***
        return str(self.value)
    def __repr__(self):
        return str(self.terms)


# class Pair():
#     def __init__(self, first, second):
#         self.first = first
#         self.second = second
#         self.value = [first, second]
#     def __eq__(self, other):
#         if isinstance(other, Pair):
#             return self.first == other.first and self.second == other.second
#         else:
#             if isinstance(other, Var):

    def __str__(self):
        return str(self.first) + "-" + str(self.second)
    def __repr__(self):
        return str(self)


# # A Pair is a combination of terms seperated with dashes. 
# class Pair(ListPL):
#     def __init__(self, terms):
#         self.head = terms[0]
#         if len(terms) > 2:
#             self.tail = Pair(terms[1:])
#         else:
#             self.tail = Const(terms[1])
#         self.terms = terms
#         Term.__init__(self, name = "Pair", value = self.terms)
#     def __str__(self):
#         return "-".join(str(term) for term in self.terms)


def tryGoal(goal):
    if isinstance(goal, Var):
        goal = goal.value
    wasCut = False
    # Keep copy of original goal args. This is not a deep copy, so changed values will remain changed here.
    # This allows Vars that are temporary changed to Consts to return back to their Var form.
    originalArgs = [arg for arg in goal.args]
    if len(goal.args) in goal.pred.alternatives:
        alts = goal.pred.alternatives[len(goal.args)]       # The list of all alts with matching arity.
        # If a variable already has a value, this goal cannot change it.
        # To ensure the value does not get reset, the variable must be changed to a Const.
        for argIndex, arg in enumerate(goal.args):
            if isinstance(arg, Var) and arg.value != "Undefined":
                goal.args[argIndex] = Term.changeType(arg.value)
        # Only yield if it succeeded, since failing one alt doesn't mean that the goal failed.
        for alt in alts:
            altAttempts = tryAlt(goal, alt)
            # Only yield if it succeeded, since failing one alt doesn't mean that the goal failed.
            for attempt in altAttempts:
                success = attempt[0]
                wasCut = attempt[1]
                if success:
                    # Yield vars, or True if this succeeded without changing vars.
                    yield (findVars(goal.args) or True, wasCut)
                if wasCut:
                    break
            # Clear any args that were defined in this goal, so they may be reused for the next alt.
            for arg in goal.args:
                if isinstance(arg, Var):
                    changePath(arg, "Undefined")
            if wasCut:
                wasCut = False
                break
    # If no predicate exists with this number of arguments, it may be a built-in predicate.
    elif goal.pred == write_ and len(goal.args) == 1:
        print(flatten(goal.args[0].value), end="")
        yield True, wasCut
    elif goal.pred == nl_:
        print()
        yield True, wasCut
    elif goal.pred == lt_:
        yield (goal.args[0].value < goal.args[1].value, wasCut)
    elif goal.pred == le_:
        yield (goal.args[0].value <= goal.args[1].value, wasCut)
    elif goal.pred == gt_:
        yield (goal.args[0].value > goal.args[1].value, wasCut)
    elif goal.pred == ge_:
        yield (goal.args[0].value >= goal.args[1].value, wasCut)
    elif goal.pred == cut:
        wasCut = True
        yield True, wasCut
    elif goal.pred == setEqual:
        if tryUnify([goal.args[0]], [goal.args[1]]):
            yield (findVars(goal.args) or True, wasCut)
    elif goal.pred == notEqual:
        if goal.args[0].value != goal.args[1].value:
            yield (findVars(goal.args) or True, wasCut)
    elif goal.pred == call_:
        goalToCall = goal.args[0].value
        result = next(tryGoal(goalToCall))
        yield (result[0], wasCut)
    # After trying all alts, reset any Vars that were turned into Consts.
    goal.args = originalArgs
    yield False, wasCut               # If all the alts failed, then the goal failed.


# This tries the current alternative to see if it succeeds.
def tryAlt(query, alt):
    wasCut = False
    # Memo is a dictionary of all terms in this alt.
    # This makes sure that no terms are duplicates.
    memo = {}
    altArgs = [create(arg, memo) for arg in alt.args]
    altGoals = [create(goal, memo) for goal in alt.goals]
    goalsToTry = altGoals          # A list of goals that must be satisfied for this alt to succeed.
    if not tryUnify(query.args, altArgs):    # If the alt can't be unified, then it fails.
        yield False, wasCut
    elif len(goalsToTry) > 0:       # If this alt has goals, try them.
        for attempt in tryGoals(goalsToTry):
            wasCut = attempt[1]
            yield attempt
            if wasCut:
                break
    else:
        yield True, wasCut  # If there are no goals to try, this alt succeeded.


def tryGoals(goalsToTry):
    wasCut = False
    goals = [tryGoal(goal) for goal in goalsToTry]  # A list of [tryGoal(goal1), tryGoal(goal2), etc]
    currGoal = 0                                    # This is the index for the goal we are currently trying.
    failed = False
    while not failed:
        while 0 <= currGoal < len(goals):           # The goals succeed it currGoal reaches the end.
            if wasCut and goalsToTry[currGoal].pred == cut:
                failed = True
                break
            if goalsToTry[currGoal].pred == cut:
                wasCut = True
            currGoalAttempt = next(goals[currGoal])
            success = currGoalAttempt[0]
            wasCut = currGoalAttempt[1]
            if success:                        # This goal succeeded and args have been instantiated.
                currGoal += 1
            else:
                if currGoal == 0 or wasCut:   # If the first goal fails, there are no more things to try, and the function fails.
                    failed = True
                    break
                goals[currGoal] = tryGoal(goalsToTry[currGoal])  # Reset the generator.
                currGoal -= 1
        if not failed:
            yield True, wasCut     # If we got here, then all the goals succeeded.
            currGoal -= 1       # Go back a goal to try for another solution.
    yield False, wasCut


def changePath(arg, newValue):
    if isinstance(arg, Var):
        arg.value = newValue
    for child in arg.children:
        # if child value already is new value, maybe don't need to change child's path? Try later! ***
        changePath(child, newValue)         # Change each parent to the new value.


# Returns a list of all Vars found in a list.
def findVars(args):
    result = []
    for arg in args:
        if isinstance(arg, ListPL):
            result.extend(findVars(arg.value))
        if isinstance(arg, Var) and arg.name[0] != "_":
            if isinstance(arg.value, list):
                arg = Var(arg.name, arg.value)
            result.append(arg)
    return result


# This flattens a list with "|" into a list with values, not terms.
def flatten(toFlatten):
    if not isinstance(toFlatten, list):
        return toFlatten
    lst = toFlatten[:]
    if len(lst) > 2 and lst[-2].value == "|":
        tail = lst.pop()
        lst.pop()
        lst.extend(flatten(tail.value))
    return [item.value if isinstance(item, Term) else item for item in lst]


# Turn a string of a Goal into a goal.
# Before doing this, remove spaces from input and split input by ",". Then call with each element. ***
def goalFromString(strOfGoals):   
    strOfGoals = strOfGoals.replace(" ", "")             # Remove spaces.
    if strOfGoals[-1:] != ")":               # No matter how many goals there are, there should always be a ")" at the end.
        raise Exception("Goals must end with ')'")
    else:
        strOfGoals = strOfGoals[:-1]        # Remove the ")" at the end.
    lstOfGoals = strOfGoals.split("),")     # If there are multiple goals, separate them. This removes the ")" from each goal.
    for index, goal in enumerate(lstOfGoals):
        currGoal = goal.split("(")          # Split the goal into its name and arguments.
        predName = currGoal[0]
        if predName in preds:
            args = currGoal[1].split(",")   # Seperate the args.
            # Remove extra " or ' from each arg if there is one.
            args = [arg[1:-1] if (arg[0] == "'" and arg[-1] == "'") or (arg[0] == '"' and arg[-1] == '"') else arg for arg in args]
            # args = [arg.strip() for arg in args]
            lstOfGoals[index] = preds[predName](*args)    # Replace string of goal with actual goal.
        else:
            raise Exception("Predicate not found: " + predName)
    return lstOfGoals


# # This can be used to query similarly to Prolog. 
# # Type ";" to continue, "." to query again, and "halt" to end.
# def beginQuerying():
#     while True: 
#         queryInput = input("?- ")       # Here, a user should input a goal. For example: between(2, 6, "X")
#         goals = goalFromString(queryInput)
#         count = 0                       # This keeps track of the current solution we are on.
#         query = Query()                 # Reset the current query.
#         query << goals                  # Add the goals to the query.
#         print(query[count])             # Show the first solution.
#         queryInput = input("?- ")       # Get input to see what to do next.
#         while queryInput == ";":        # If it's a semicolon, show the next solution.
#             count += 1                  # Increment the solution count.
#             try:
#                 print(query[count])         # Print the next solution
#                 queryInput = input("?- ")   # Get input to see if the query should continue.
#             except:
#                 print("No more solutions.")
#                 break
#         if queryInput == "halt":        # If it's "halt", the function ends.
#             break



# This can be used to query similarly to Prolog. 
# Type ";" to continue, "." to query again, and "halt" to end.
def beginQuerying():
    while True: 
        queryInput = input("?- ")       # Here, a user should input a goal. For example: between(2, 6, "X")
        if queryInput == "halt":        # If it's "halt", the function ends.
            break
        elif queryInput == ";":         # If it's ";", the function shows the next solution.
            count += 1
            try:
                print(query[count])         # Print the next solution
                # queryInput = input("?- ")   # Get input to see if the query should continue.
            except:
                print("No more solutions.")
        else:       # If it's anything else, it's a query.        
            goals = goalFromString(queryInput)
            count = 0                       # This keeps track of the current solution we are on.
            query = Query()                 # Reset the current query.
            query << goals                  # Add the goals to the query.
            print(query[count])             # Show the first solution.


# #### Built-in Features ####

# Use to make queries.
query = Query()


# Mathamatical expressions that can be used.
# To use these, type the operator between two |s, like so:
# 4 |plus| 5 |plus| 6
plus = Math(lambda x, y: x + y)
minus = Math(lambda x, y: x - y)
times = Math(lambda x, y: x * y)
div = Math(lambda x, y: x / y)
floorDiv = Math(lambda x, y: x // y)
mod = Math(lambda x, y: x % y)

# The Prolog is/2 predicate.
is_ = Predicate("is_")
is_("Q", "Q") >> []

# fail/0.
fail_ = Predicate("fail_")

write_ = Predicate("write_")
nl_ = Predicate("nl_")

member_ = Predicate("member_")
member_("H", ["H", "|", "_"]) >> []
member_("H", ["_", "|", "T"]) >> [member_("H", "T")]

append_ = Predicate("append_")
append_([], "W", "W") >> []
append_(["H", "|", "T"], "X", ["H", "|", "S"]) >> [append_("T", "X", "S")]


# cut (!) predicate.
cut = Predicate("cut")

# =/2 predicate.
setEqual = Predicate("setEqual")
notEqual = Predicate("notEqual")

call_ = Predicate("call_")


not_ = Predicate("not_")
not_("A") >> [call_("A"), cut(), fail_()]
not_("_") >> []


# </2 predicate.
lt_ = Predicate("less than")
le_ = Predicate("less than or equal")
gt_ = Predicate("greater than")
ge_ = Predicate("greater than or equal")


between = Predicate("between")
between("N", "M", "K") >> [le_("N", "M"), setEqual("K", "N")]
between("N", "M", "K") >> [lt_("N", "M"), is_("N1", "N" |plus| 1), between("N1", "M", "K")]


len_ = Predicate("len_")
len_([], 0) >> []
len_(["_", "|", "T"], "A") >> [len_("T", "B"), is_("A", "B" |plus| 1)]


permutation_ = Predicate("permutation_")
permutation_([], []) >> []
permutation_(["H", "|", "T"], "S") >> [permutation_("T", "P"), append_("X", "Y", "P"), append_("X", ["H", "|", "Y"], "S")]


reverse_ = Predicate("reverse_")
reverse_("Xs", "Ys") >> [reverse_("Xs", [], "Ys", "Ys")]
reverse_([], "Ys", "Ys", []) >> []
reverse_(["X", "|", "Xs"], "Rs", "Ys", ["_", "|", "Bound"]) >> [reverse_("Xs", ["X", "|", "Rs"], "Ys", "Bound")]

# This is used when head should always succeed. ***
true_ = Predicate("true_")


# beginQuerying()
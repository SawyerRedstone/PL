# The PL Module offers Prolog functionality for Python programmers.
# Created by Sawyer Redstone.

import itertools

# Take a list, string, or int, and convert it to type Term.
def create(term, memo = {}):
    if str(term) in memo:
        return memo[str(term)]
    if isinstance(term, int) or isinstance(term, float):   # Numbers are constants.
        memo[str(term)] = Const(term)
    elif isinstance(term, list):
        # If the list is empty, it is a Const; otherwise it is a ListPL.
        memo[str(term)] = ListPL([create(item, memo) for item in term]) if term else Const(term)
    elif isinstance(term, Goal):
        if term.name == "format_":
            strToWrite = term.args[0]      # The string to write, with {} in places that can be filled with vars.
            if len(term.args) > 1:
                vars = [create(arg, memo) for arg in term.args[1]]  # The vars to fill in the string.
            else:
                vars = []
            memo[str(term)] = Goal(term.pred, [strToWrite, vars])
        else:
            memo[str(term)] = Goal(term.pred, [create(arg, memo) for arg in term.args])
    elif term[0].isupper() and " " not in term:
        memo[str(term)] = Var(term)
    elif term[0] == "_":        # Vars that start with "_" are temporary.
        return Var(term)        # Since all _s are different, they should not be added to memo.
    # Otherwise, it is a Const.
    else:
        # If string has single quotes around it, remove them.
        if term[0] == "'" and term[-1] == "'":
            term = term[1:-1]
            memo[str(term)] = Const(term)
        elif " " in term:
            math = Math()
            math.mathToList(term, memo)
            memo[str(term)] = math
        else:       # Maybe if it is the string of a num, turn it into the num.
            try:
                memo[str(term)] = Const(int(term))
            except ValueError:
                try:
                    memo[str(term)] = Const(float(term))
                except ValueError:
                    memo[str(term)] = Const(term)
    return memo[str(term)]


class Predicate():
    def __init__(self, name):
        self.name = name            # The name of the predicate
        self.alternatives = {}      # Dict filled with all of the predicate alternatives, with arity as key.
    def __repr__(self):
        return self.name
    def __call__(self, *args):
        return Goal(self, args)


# Use query << [list of goals] for queries.
# Once the query is made, Query becomes a list of all the results.
class Query(list):
    def __init__(self):
        self.goals = []
        self.size = None
        super().__init__()
    def __lshift__(self, goals):
        # Reset the query. 
        self.clear()        
        # Memo is a dictionary of all args in the goals.
        # This makes sure that no terms are duplicates.
        memo = {}
        goals = [create(goal, memo) for goal in goals]
        attempt = tryGoals(goals)
        # Loop through the generator self.size times, or until end if size is not specified.
        for attempt in itertools.islice(attempt, self.size):
            success = attempt[0]
            wasCut = attempt[1]
            if not success:     # Check if this can be removed so False shows up. ***
                break
            args = {}
            for argName in memo:
                if isinstance(memo[argName], Var):
                    args[argName] = str(flatten(memo[argName].value))
            if len(args) > 0:
                self.append(args)
            else:
                self.append(True)
            if wasCut:
                break
        if self == []:
            self.append(False)
        # Reset the size for future queries, in the case where multiple queries are made at once.
        self.size = None
    # query(3) makes the query only show 3 results.
    def __call__(self, num):
        self.size = num
        return self

# Goals must be completed in order to satisfy a query.
class Goal():
    def __init__(self, pred = [], args = []):       # Maybe change, since preds can't be empty. ***
        self.name = pred.name
        self.pred = pred            # The predicate that is being queried.
        self.args = list(args)      # Create a list of the goal's arguments.
        self.value = self           # This allows goals to unify with Vars.
    def __str__(self):
        return "goalPred: " + self.name + "\nGoalArgs: " + str(self.args) + "\n"
    # Add facts as: head >> []
    # Add rules as: head >> [goal1, goal2, ...]
    def __rshift__(self, others):
        if len(self.args) in self.pred.alternatives:
            self.pred.alternatives[len(self.args)].append(Alt(self.pred, self.args, others))
        else:
            self.pred.alternatives[len(self.args)] = [Alt(self.pred, self.args, others)]
    def __repr__(self):
        return self.name
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
        super().__init__(name = value, value = value)



class Math(Term):
    def __init__(self):
        self.mathList = []
        self.children = []
    @property
    def value(self):
        toEval = self.mathList[:]
        for i in range(len(toEval)):
            if isinstance(toEval[i], Term):
                name = toEval[i].name
                try:
                    toEval[i] = toEval[i].value
                    # Make sure that the value is a number.
                    if not isinstance(toEval[i], (int, float)):
                        raise TypeError
                except:
                    raise ValueError("'" + name + "' doesn't have a numeric value.")
        return eval("".join([str(term) for term in toEval]))
    # This takes a string of math and turns it into a list of numbers and operators
    def mathToList(self, mathStr, memo = {}):
        # Add more operators here! ***
        mathStr = mathStr.replace(" ", "")
        mathStr = mathStr.replace("+", " + ")
        mathStr = mathStr.replace("-", " - ")
        mathStr = mathStr.replace("*", " * ")
        mathStr = mathStr.replace("**", " ** ")
        mathStr = mathStr.replace("^", " ** ")        # Prolog style for exponentiation.
        mathStr = mathStr.replace("/", " / ")
        mathStr = mathStr.replace("//", " // ")
        mathStr = mathStr.replace("(", " ( ")
        mathStr = mathStr.replace(")", " ) ")
        mathStr = mathStr.replace("%", " % ")
        mathStr = mathStr.replace("mod", " % ")   # Prolog style for modulo.
        self.mathList = mathStr.split()
        for i in range(len(self.mathList)):
            if self.mathList[i] not in ["+", "-", "*", "**", "/", "//", "(", ")", "%", "mod"]:
                self.mathList[i] = create(self.mathList[i], memo)


class ListPL(Term):
    def __init__(self, terms, name = "List"):
        self.head = terms[0]
        self.tail = Term.changeType(terms[1:])
        self.terms = terms      # The list of terms before they were seperated into a head and tail.
        super().__init__(name = name, value = terms)
    def __len__(self):
        return len(self.value)
    def __eq__(self, other):
        if isinstance(other.value, list) and other.value:
            other = ListPL(other.value)
        if self.tail and not isinstance(self.tail, ListPL):
            self.tail = Term.changeType(self.tail.value)
        if isinstance(other, ListPL):
            return self.head == other.head and self.tail == other.tail
        return super().__eq__(other)
    def unifyWith(self, altArg):
        if isinstance(altArg.value, list) and altArg.value:
            altArg = ListPL(altArg.value)
        if isinstance(altArg, ListPL):
            if self.head.unifyWith(altArg.head) and self.tail.unifyWith(altArg.tail):
                return True
            return False
        return super().unifyWith(altArg)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.terms)


def tryGoal(goal):
    if isinstance(goal, Var):
        goal = goal.value
    wasCut = False
    # Make the goal a copy of itself, so that changing args here doesn't mess up the original args.
    goal = Goal(goal.pred, goal.args)   
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
    elif goal.pred == format_:
        strToWrite = goal.args[0]
        varsToFill = [flatten(arg.value) for arg in goal.args[1]]
        print(strToWrite.format(*varsToFill), end="")
        yield True, wasCut
    elif goal.pred == write:
        print(flatten(goal.args[0].value), end="")
        yield True, wasCut
    elif goal.pred == nl:
        print()
        yield True, wasCut
    elif goal.pred == lt:
        yield (goal.args[0].value < goal.args[1].value, wasCut)
    elif goal.pred == le:
        yield (goal.args[0].value <= goal.args[1].value, wasCut)
    elif goal.pred == gt:
        yield (goal.args[0].value > goal.args[1].value, wasCut)
    elif goal.pred == ge:
        yield (goal.args[0].value >= goal.args[1].value, wasCut)
    elif goal.pred == cut:
        wasCut = True
        yield True, wasCut
    elif goal.pred == notEqual:
        if goal.args[0].value != goal.args[1].value:
            yield (findVars(goal.args) or True, wasCut)
    elif goal.pred == call:
        goalToCall = goal.args[0].value
        # Make the called goal a copy of itself, so that changing args here doesn't mess up the original args.
        goalToCall = Goal(goalToCall.pred, goalToCall.args)
        result = next(tryGoal(goalToCall))
        yield (result[0], wasCut)
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


# #### Built-in Features ####

# Use to make queries.
query = Query()

# Evaluates both sides and then tries to unify.
equals = Predicate("equals")
equals("Q", "Q") >> []

# fail/0.
fail = Predicate("fail")

# write/1.
write = Predicate("write")

# format/2: arg1 is a string with {}s for vars and arg2 is a list of vars.
# e.g. format_("{} likes you.", ["X"]) or format_("{}", ["X"]).
format_ = Predicate("format_")

nl = Predicate("nl")

member = Predicate("member")
member("H", ["H", "|", "_"]) >> []
member("H", ["_", "|", "T"]) >> [member("H", "T")]

append = Predicate("append")
append([], "W", "W") >> []
append(["H", "|", "T"], "X", ["H", "|", "S"]) >> [append("T", "X", "S")]


# cut (!) predicate.
cut = Predicate("cut")

# \=/2 predicate.
notEqual = Predicate("notEqual")

# This allows a goal to be used as an argument for another goal.
call = Predicate("call")

# \+/1 predicate.
not_ = Predicate("not_")
not_("A") >> [call("A"), cut(), fail()]
not_("_") >> []


# The comparison predicates.
lt = Predicate("less than")
le = Predicate("less than or equal")
gt = Predicate("greater than")
ge = Predicate("greater than or equal")


between = Predicate("between")
between("N", "M", "K") >> [le("N", "M"), equals("K", "N")]
between("N", "M", "K") >> [lt("N", "M"), equals("N1", "N + 1"), between("N1", "M", "K")]


length = Predicate("length")
length([], 0) >> []
length(["_", "|", "T"], "A") >> [length("T", "B"), equals("A", "B + 1")]


permutation = Predicate("permutation")
permutation([], []) >> []
permutation(["H", "|", "T"], "S") >> [permutation("T", "P"), append("X", "Y", "P"), append("X", ["H", "|", "Y"], "S")]


reverse = Predicate("reverse")
reverse("Xs", "Ys") >> [reverse("Xs", [], "Ys", "Ys")]
reverse([], "Ys", "Ys", []) >> []
reverse(["X", "|", "Xs"], "Rs", "Ys", ["_", "|", "Bound"]) >> [reverse("Xs", ["X", "|", "Rs"], "Ys", "Bound")]


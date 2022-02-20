# The PL Module offers Prolog functionality for Python programmers.
# Created by Sawyer Redstone.

# This will take a list, for example ["A", "C"], and convert all the strings to Terms.
def stringsToTerms(oldList, memo = {}):     # Memo is a dict of terms already created
    newList = []
    for word in oldList:
        # Represent duplicate strings as the same Term.
        if str(word) in memo:
            nextWord = memo[str(word)]
        elif isinstance(word, list):
            if "|" not in word:
                word.append("[]")
            recursed = stringsToTerms(word, memo)
            memo[str(word)] = Const(recursed)       # Const can hold a list.
            nextWord = memo[str(word)]
        # Anything with a space Math.
        elif ' ' in word:
            parts = word.split()
            parts = [memo[part] if part in memo else part for part in parts]
            memo[word] = Math(word, parts)
            nextWord = memo[word]
        # If the first letter is uppercase or _, it is a Var.
        elif word[0].isupper() or word[0] == "_":    # Does _ work???
            word = str(word)
            memo[word] = Var(word)
            nextWord = memo[word]
        # All other strings are Consts.
        else:
            word = str(word)
            memo[word] = Const(word)
            nextWord = memo[word]
        newList.append(nextWord)
    return newList


class Predicate(): 
    def __init__(self, name): 
        self.name = name            # The name of the predicate
        self.alternatives = {}      # Dict filled with all of the predicate alternatives, with arity as key.
    def __repr__(self):
        return self.name
    def __call__(self, *args):
        return Goal(self, args)



# Goals must be completed in order to satisfy a query.
class Goal():
    def __init__(self, pred = [], args = []):
        self.pred = pred           # The predicate that is being queried.
        self.args = list(args)          # Create a list of the goal's arguments.
    def __str__(self):
        return "goalPred: " + self.pred.name + "\nGoalArgs: " + str(self.args) + "\n"
    def __rshift__(self, others):
        if len(self.args) in self.pred.alternatives:
            self.pred.alternatives[len(self.args)].append(Alt(self.args, others))
        else:
            self.pred.alternatives[len(self.args)] = [Alt(self.args, others)]
    # '+' for putting info IN, AKA adding facts.
    def __pos__(self):
        self >> []
    # '-' for getting info OUT, AKA making queries.
    def __neg__(self):
        self.args = stringsToTerms(self.args)
        for success in tryGoal(self):
            yield success



# Alts are individual alternatives that were added to a predicate.
class Alt():
    def __init__(self, args, goals): 
        self.args = args  
        self.goals = goals
    def __str__(self):
        return "altArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))

# This function tries to unify the query and alt args, and returns a bool of its success.
def tryUnify(queryArgs, altArgs):
    for index, (queryArg, altArg) in enumerate(zip(queryArgs, altArgs)):    # Loop through the query and alt arguments.
        if queryArg.value == "|" and altArg.value == "|":
            return queryArgs[-1].unifyWith(altArg[-1])
        elif queryArg.value == "|":
            # return queryArgs[-1].unifyWith(Const(altArgs[index:]))
            if queryArgs[-1].unifyWith(Const(altArgs[index:])):     # Need to empty these from altArgs!!???
                tail = queryArgs.pop()
                queryArgs.pop()
                queryArgs.extend(tail.value)
                # del altArgs[index:]
            else:
                return False
        elif altArg.value == "|":
            # return Const(queryArgs[index:]).unifyWith(altArgs[-1])
            if Const(queryArgs[index:]).unifyWith(altArgs[-1]):
                tail = altArgs.pop()
                altArgs.pop()
                altArgs.extend(tail.value)
                # del queryArgs[index:]
            else:
                return False
        # Check if unification is possible before unifying.
        if isinstance(queryArg.value, list) and isinstance(altArg.value, list):
            tryUnify(queryArg.value, altArg.value)
        if queryArg != altArg:                  # Is this a problem if the fail occures in middle of unifying???
            return False
        queryArg.unifyWith(altArg)
    return True                                 # If it reaches this point, they can be unified.   


# Variables and Constants are Terms.
class Term():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []                  # The children are the variables that will change if this term has a value.
    # This checks if they *can* be equal.
    def __eq__(self, other):
        # if isinstance(self.value, list) and isinstance(other.value, list):
            # ???
        return self.value == other.value or not self or not other
    def __bool__(self):
        return self.value != "Undefined"    # A term is false it if has no value.
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))    
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
        super().__init__(name = name, value = value)    # Initialize the Var.


class Const(Term):  # A constant, aka an atom.
    def __init__(self, value):
        super().__init__(name = "Const", value = value)
    def __repr__(self):
        return str(self.value)

class Math(Term):        # This is a number or mathematical expression.
    def __init__(self, name, terms):
        self.terms = terms
        super().__init__(name = name, value = "Undefined")
    # Find their value and check if equal.
    def __eq__(self, other):
        try:
            self.value = str(self)
            if isinstance(other, Math):
                other.value = str(other)
            return super().__eq__(other)
        # If the math doesn't make sense, return False.
        except:
            return False
    def __str__(self):
        # First turn each term into its value form.
        self.terms = [str(term) for term in self.terms]
        # Then evalute and return the results.
        result = float(eval("".join(self.terms)))
        return ('%f' % result).rstrip('0').rstrip('.')  # Strip trailing 0s.


def tryGoal(goal):
    # Keep copy of original goal args. This is not a deep copy, so changed values will remain changed here.
    # This allows Vars that are temporary changed to Consts to return back to their Var form.
    originalArgs = [arg for arg in goal.args]
    if len(goal.args) in goal.pred.alternatives:
        alts = goal.pred.alternatives[len(goal.args)]       # The list of all alts with matching arity.
        # If a variable already has a value, this goal cannot change it.
        # To ensure the value does not get reset, the variable must be changed to a Const.
        for argIndex, arg in enumerate(goal.args):
            if isinstance(arg, Var) and arg.value != "Undefined":
                goal.args[argIndex] = Const(arg.value)
        # Only yield if it succeeded, since failing one alt doesn't mean that the goal failed.
        for alt in alts:
            altAttempts = tryAlt(goal, alt)
            # Only yield if it succeeded, since failing one alt doesn't mean that the goal failed.
            for attempt in altAttempts:
                if attempt:
                    # Yield vars, or True if this succeeded without changing vars.
                    yield findVars(goal.args) or True
            # Clear any args that were defined in this goal, so they may be reused for the next alt.
            for arg in goal.args:
                if isinstance(arg, Var):
                    changePath(arg, "Undefined")
    # If no predicate exists with this number of arguments, it may be a built-in predicate.
    elif goal.pred == write and len(goal.args) == 1:
            print(goal.args[0].value)
            yield True
    elif goal.pred == setEqual:     # ???
        if tryUnify([goal.args[0]], [goal.args[1]]):
            yield findVars(goal.args) or True
    # After trying all alts, reset any Vars that were turned into Consts.
    goal.args = originalArgs
    yield False               # If all the alts failed, then the goal failed.


# This tries the current alternative to see if it succeeds.
def tryAlt(query, alt):
    # Memo is a dictionary of all terms in this alt.
    # This makes sure that no terms are duplicates.
    memo = {}       
    altArgs = stringsToTerms(alt.args, memo)
    altGoals = [Goal(goal.pred, stringsToTerms(goal.args, memo)) for goal in alt.goals if goal]
    goalsToTry = altGoals          # A list of goals that must be satisfied for this alt to succeed.
    if not tryUnify(query.args, altArgs):    # If the alt can't be unified, then it fails.
        yield False
    elif len(goalsToTry) > 0:       # If this alt has goals, try them.
        for success in tryGoals(goalsToTry):
            yield success
    else:
        yield True  # If there are no goals to try, this alt succeeded.


def tryGoals(goalsToTry):
    goals = [tryGoal(goal) for goal in goalsToTry]  # A list of [tryGoal(goal1), tryGoal(goal2), etc]
    currGoal = 0                                    # This is the index for the goal we are currently trying.
    failed = False
    while not failed:
        while 0 <= currGoal < len(goals):           # The goals succeed it currGoal reaches the end.
            currGoalArgs = next(goals[currGoal])    # Try the goal at the current index.
            if currGoalArgs:                        # This goal succeeded and args have been instantiated.
                currGoal += 1
            else:
                if currGoal == 0:   # If the first goal fails, there are no more things to try, and the function fails.
                    failed = True
                    break
                goals[currGoal] = tryGoal(goalsToTry[currGoal])  # Reset the generator.
                currGoal -= 1
        if not failed:
            yield True          # If we got here, then all the goals succeeded.
            currGoal -= 1       # Go back a goal to try for another solution.


def changePath(arg, newValue):
    if isinstance(arg, Term):
        arg.value = newValue
        for child in arg.children:
            # if child value already is new value, maybe don't need to change child's path? Try later! ???
            changePath(child, newValue)         # Change each parent to the new value.


# Returns a list of all Vars found in a list.
def findVars(args):
    result = []
    for arg in args:
        if isinstance(arg.value, list):
        # if isinstance(arg, list):     # ???
            result.extend(findVars(arg.value))
        elif isinstance(arg, Var) and arg.name[0] != "_":
            result.append(arg)
    return result



# #### Built-in Predicates ####

# The Prolog is/2 predicate, with a different name because "is" already exists in Python.
equals = Predicate("equals")
# equals.add(["Q", "Q"])
+equals("Q", "Q")

# fail/0. This works differently from other goals, as users do not need to type Goal(fail)
fail = Predicate("failPredicate")

# write/1
write = Predicate("write")

# member/2
member = Predicate("member")

+member("X", ["X", "|", "_"])
member("X", ["_", "|", "T"]) >> [member("X", "T")]

# once/1

setEqual = Predicate("setEqual")


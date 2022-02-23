class Predicate(): 
    def __init__(self, name): 
        self.name = name            # The name of the predicate
        self.alternatives = {}      # Dict filled with all of the predicate alternatives, with arity as key.
    def __repr__(self):
        return self.name
    def __call__(self, *args):
        return Goal(self, args)

class AST:				
	def __plus__(self, righthand):
		if type(righthand) == int:
			righthand = Const(righthand)
		return BinaryOperator("+", self, righthand)

class BinaryOperator(AST):
	def eval(self, env):
		if self.name == "+":
			return self.left.eval(env) + self.right.eval(env)

class Term(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []                  # The children are the variables that will change if this term has a value.
    def __eq__(self, other):
        return self.value == other.value or not self or not other
    def __bool__(self):
        return self.value != "Undefined"    # A term is false it if has no value.
    def __repr__(self):
        # return str(self.value)
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



class V:
	def __getattr__(self, name):
		return Var(name)


class C:
	def __getattr__(self, name):
		return Const(name)


# Create a Const and Var object so __getattr__ can be used.
C = C()
V = V()


class Var(Term):
    def __init__(self, name, value = "Undefined"):
        super().__init__(name = name, value = value)    # Initialize the Var. 
    def eval(self, env):
        # if self.name in env:
        #     return env[self.name]
        # else:
        #     raise Error
        try:
            return env[self.name]
        except:
            print("Uh oh!")     # ???


class ListPL(Term):
    def __init__(self, lst):
        self.head = lst[0]
        self.tail = Term.create(lst[1:])
        super().__init__(name = "List", value = lst)
    def __len__(self):
        return len(self.value)
    def __eq__(self, other):
        if isinstance(other, ListPL):
            return self.head == other.head and self.tail == other.tail
        return super().__eq__(other)
    def unifyWith(self, altArg):
        if isinstance(altArg, ListPL):
            if self.head.unifyWith(altArg.head) and self.tail.unifyWith(altArg.tail):
                for term in enumerate(self.tail.value):
                    if term:
                        Term.create(term)
                return True
            return False
            # return self.head.unifyWith(altArg.head) and self.tail.unifyWith(altArg.tail)
        return super().unifyWith(altArg)
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.value)


class Alt():
    def __init__(self, args, goals): 
        # Memo is a dictionary of all terms in this alt.
        # This makes sure that no terms are duplicates.
        memo = {}       
        self.args = removeDuplicates(args, memo)
        self.goals = [Goal(goal.pred, removeDuplicates(goal.args, memo)) for goal in goals if goal]
    def __str__(self):
        return "altArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))


# Goals must be completed in order to satisfy a query.
class Goal():
    def __init__(self, pred = [], args = []):
        self.pred = pred                        # The predicate that is being queried.
        self.args = removeDuplicates(args)      # Create a list of the goal's arguments.
    def __str__(self):
        return "goalPred: " + self.pred.name + "\nGoalArgs: " + str(self.args) + "\n"
    # Add rules as: head >> [goal1, goal2]
    def __rshift__(self, others):
        if len(self.args) in self.pred.alternatives:
            self.pred.alternatives[len(self.args)].append(Alt(self.args, others))
        else:
            self.pred.alternatives[len(self.args)] = [Alt(self.args, others)]
    # '+' for putting info IN (facts). 
    def __pos__(self):
        self >> []      # Treat a fact as a rule with no goals.
    # '-' for getting info OUT (Queries).
    def __neg__(self):
        for success in tryGoal(self):
            yield success


class Const(Term):  # A constant, aka an atom.
    def __init__(self, value):
        # super().__init__(name = "Const", value = value)
        super().__init__(name = value, value = value)
    def __repr__(self):
        return str(self.value)


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
                goal.args[argIndex] = Term.create(arg.value)
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
    altArgs = removeDuplicates(alt.args, memo)
    altGoals = [Goal(goal.pred, removeDuplicates(goal.args, memo)) for goal in alt.goals if goal]
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


# This function tries to unify the query and alt args, and returns a bool of its success.
def tryUnify(queryArgs, altArgs):
    for queryArg, altArg in zip(queryArgs, altArgs):    # Loop through the query and alt arguments.
        # Check if unification is possible before unifying.
        if queryArg != altArg:                  # Is this a problem if the fail occures in middle of unifying???
            return False
        queryArg.unifyWith(altArg)
    return True                                 # If it reaches this point, they can be unified.   


def changePath(arg, newValue):
    if isinstance(arg, Term):
        arg.value = newValue
        for child in arg.children:
            # if child value already is new value, maybe don't need to change child's path? Try later! ???
            changePath(child, newValue)         # Change each parent to the new value.


# This unifies all Vars that share a name in a list.
def removeDuplicates(oldList, memo = {}):
    newList = []
    for term in oldList:
        if term.name not in memo:
            # Rather than changing the original term, make a copy of it.
            memo[term.name] = type(term)(term.name)
        nextTerm = memo[term.name]
        newList.append(nextTerm)
    return newList

# Returns a list of all Vars found in a list.
def findVars(args):
    result = []
    for arg in args:
        if isinstance(arg, ListPL):
            result.extend(findVars(arg.value))
        if isinstance(arg, Var) and arg.name[0] != "_":
            if isinstance(arg.value, list):
                arg.value = flatten(arg.value)
            result.append(arg)
    return result


# This flattens a list with "|"
def flatten(lst):
    if len(lst) > 2 and lst[-2].value == "|":
        tail = lst.pop()
        lst.pop()
        lst.extend(flatten(tail.value))
    return [Term.create(term.value) for term  in lst]


# #### Built-in Predicates ####

# The Prolog is/2 predicate, with a different name because "is" already exists in Python.
equals = Predicate("equals")
+equals(V.Q, V.Q)

# fail/0. This works differently from other goals, as users do not need to type Goal(fail)
fail = Predicate("failPredicate")

write = Predicate("write")

# member = Predicate("member")

# +member(V.X, [V.X, "|", V._])
# member(V.X, [V._, "|", V.T]) >> [member(V.X, V.T)]

# once/1

setEqual = Predicate("setEqual")    #???

# # Use this for all comparisons, such as >, =, 
# compare = Predicate("compare")

evaluate = Predicate("evaluate")


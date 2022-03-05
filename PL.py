# The PL Module offers Prolog functionality for Python programmers.
# Created by Sawyer Redstone.

wasCut = False

# Take a list, string, or int, and convert it to type Term.
def create(term, memo = {}):
    if str(term) in memo:
        return memo[str(term)]
    if isinstance(term, int) or isinstance(term, float):   # Numbers are constants.
        memo[str(term)] = Const(term)
    elif isinstance(term, Math):
        # Make new math term so each alt has unchanged starting math.
        newMath = Math("newMath", term.function)
        newMath.mathList = [create(item, memo) if not callable(item) else item for item in term.mathList]
        memo[str(term)] = newMath
    elif isinstance(term, list):
        # If the list is empty, it is a Const; otherwise it is a ListPL.
        memo[str(term)] = ListPL([create(item, memo) for item in term]) if term else Const(term)
    elif isinstance(term, Goal):
        memo[str(term)] = term  #???
        ###########
    elif term[0].isupper() or term[0] == "_":    # Does _ work???
        memo[str(term)] = Var(term)
    # Otherwise, it is a Const.
    else:
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



# # Goals must be completed in order to satisfy a query.
# class Goal():           # Maybe make this a Const subclass???
#     def __init__(self, pred = [], args = []):
#         self.pred = pred            # The predicate that is being queried.
#         self.args = list(args)      # Create a list of the goal's arguments.
#         self.value = str(self)      # This allows goals to unify with others.
#     def __str__(self):
#         return "goalPred: " + self.pred.name + "\nGoalArgs: " + str(self.args) + "\n"
#     # Add rules as: head >> [goal1, goal2]
#     def __rshift__(self, others):
#         if len(self.args) in self.pred.alternatives:
#             self.pred.alternatives[len(self.args)].append(Alt(self.args, others))
#         else:
#             self.pred.alternatives[len(self.args)] = [Alt(self.args, others)]
#     # '+' for putting info IN (facts). 
#     def __pos__(self):
#         self >> []      # Treat a fact as a rule with no goals.
#     # '-' for getting info OUT (Queries).
#     def __neg__(self):
#         global wasCut
#         memo = {}
#         self.args = [create(arg, memo) for arg in self.args]
#         for success in tryGoal(self):
#             yield success
#             if wasCut:
#                 wasCut = False
#                 break


# Alts are individual alternatives that were added to a predicate.
class Alt():
    def __init__(self, args, goals): 
        self.args = args  
        self.goals = goals
        # self.wasCut = False
    def __str__(self):
        return "altArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))


# This function tries to unify the query and alt args, and returns a bool of its success.
def tryUnify(queryArgs, altArgs):
    for queryArg, altArg in zip(queryArgs, altArgs):    # Loop through the query and alt arguments.
        # Check if unification is possible before unifying.
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
    def doMath(self):
        if isinstance(self.value, int) or isinstance(self.value, float):
            return self.value
        else:
            raise "Something here isn't a number..."    # Fix this later. ???
    
        
class Var(Term):
    def __init__(self, name, value = "Undefined"):
        super().__init__(name = name, value = value)    # Initialize the Var. 


class Const(Term):  # A constant, aka an atom.
    def __init__(self, value):
        super().__init__(name = "Const", value = value)
    def __repr__(self):
        return str(self.value)



# Goals must be completed in order to satisfy a query.
class Goal(Const):           # Maybe make this a Const subclass???
    def __init__(self, pred = [], args = []):
        self.pred = pred            # The predicate that is being queried.
        self.args = list(args)      # Create a list of the goal's arguments.
        super().__init__(value = str(self))
        # super().__init__(value = self)

        # self.value = str(self)      # This allows goals to unify with others.
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
        global wasCut
        memo = {}
        self.args = [create(arg, memo) for arg in self.args]
        for success in tryGoal(self):
            yield success
            if wasCut:
                wasCut = False
                break


# To use math, write the operation surrounded with |. 
# For example, '3 + 4' would be written as '3 |plus| 4'.
# (Idea from: https://code.activestate.com/recipes/384122/)
class Math(Term):
    def __init__(self, name, function):
        self.name = name
        self.value = "Undefined"
        self.mathList = []
        self.function = function
        super().__init__(name = self.name, value = "Undefined")
    def __ror__(self, other):
        # Make a new Math object so built-in objects won't change.
        newMath = Math("newbie", self.function)
        newMath.mathList = [other, self.function]
        return newMath
    def __or__(self, other):
        # Check if 'other' is built-in. (Add other built-in here! ???)
        if other is plus or other is minus:
            other = other.function
        if self.mathList[-1] is times or self.mathList[-1] is div or self.mathList[-1] is mod:
            op = self.mathList.pop()
            addend = self.mathList.pop()
            newMath = addend | op | other
            self.mathList.append(newMath)
        self.mathList.append(other)
        return self
    def doMath(self):
        result = self.mathList[0].doMath()
        for index, item in enumerate(self.mathList):
            if callable(item):
                addend = self.mathList[index+1].doMath()
                result = item(result, addend)
        self.value = result
        return result
    def __eq__(self, other):
        self.doMath()
        # other.doMath()    # ???
        return super().__eq__(other)
    def __str__(self):
        return self.name + ": " + str(self.mathList)
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(tuple(self.mathList))
    # def clear(self):    # Maybe use this to clear changed values.
    #     pass

plus = Math("plus", lambda x, y: x + y)
minus = Math("plus", lambda x, y: x - y)
times = Math("times", lambda x, y: x * y)
div = Math("div", lambda x, y: x / y)
mod = Math("mod", lambda x, y: x % y)


# This flattens a list with "|"
def flatten(lst):
    if len(lst) > 2 and lst[-2].value == "|":
        tail = lst.pop()
        lst.pop()
        lst.extend(flatten(tail.value))
    return [Term.changeType(term.value) for term in lst]


class ListPL(Term):
    def __init__(self, lst):
        self.head = lst[0]
        self.tail = Term.changeType(lst[1:])
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
                        Term.changeType(term)
                return True
            return False
            # return self.head.unifyWith(altArg.head) and self.tail.unifyWith(altArg.tail)
        return super().unifyWith(altArg)
    def __repr__(self):
        return str(self)
    def __str__(self):
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
                goal.args[argIndex] = Term.changeType(arg.value)
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
                # if isinstance(arg, Var) or isinstance(arg, Math):
                if isinstance(arg, Var):
                    changePath(arg, "Undefined")
                # elif isinstance(arg, list):   # probably should add this.
    # If no predicate exists with this number of arguments, it may be a built-in predicate.
    elif goal.pred == write and len(goal.args) == 1:
            print(goal.args[0].value)
            yield True
    elif goal.pred == lt_:
        yield goal.args[0].doMath() < goal.args[1].doMath()
    elif goal.pred == le_:
        yield goal.args[0].doMath() <= goal.args[1].doMath()
    elif goal.pred == gt_:
        yield goal.args[0].doMath() > goal.args[1].doMath()
    elif goal.pred == ge_:
        yield goal.args[0].doMath() >= goal.args[1].doMath()
    elif goal.pred == cut:
        global wasCut
        wasCut = True
        yield True
    elif goal.pred == setEqual:     # ???
        if tryUnify([goal.args[0]], [goal.args[1]]):
            yield findVars(goal.args) or True
    elif goal.pred == notEqual:
        if goal.args[0].value != goal.args[1].value:
            yield findVars(goal.args) or True
    # After trying all alts, reset any Vars that were turned into Consts.
    goal.args = originalArgs
    yield False               # If all the alts failed, then the goal failed.


# This tries the current alternative to see if it succeeds.
def tryAlt(query, alt):
    # Memo is a dictionary of all terms in this alt.
    # This makes sure that no terms are duplicates.
    memo = {}       
    altArgs = [create(arg, memo) for arg in alt.args]
    altGoals = [Goal(goal.pred, [create(arg, memo) for arg in goal.args]) if isinstance(goal, Goal) else goal for goal in alt.goals]
    goalsToTry = altGoals          # A list of goals that must be satisfied for this alt to succeed.
    if not tryUnify(query.args, altArgs):    # If the alt can't be unified, then it fails.
        yield False
    elif len(goalsToTry) > 0:       # If this alt has goals, try them.
        for success in tryGoals(goalsToTry):
            yield success
    else:
        yield True  # If there are no goals to try, this alt succeeded.


def tryGoals(goalsToTry):
    # global wasCut
    goals = [tryGoal(goal) if isinstance(goal, Goal) else create(goal) for goal in goalsToTry]  # A list of [tryGoal(goal1), tryGoal(goal2), etc]
    # goals = [tryGoal(goal.value) if isinstance(goal, Goal) else create(goal) for goal in goalsToTry]  # A list of [tryGoal(goal1), tryGoal(goal2), etc]

    currGoal = 0                                    # This is the index for the goal we are currently trying.
    failed = False
    while not failed:
        while 0 <= currGoal < len(goals):           # The goals succeed it currGoal reaches the end.
            try:
                currGoalArgs = next(goals[currGoal])   # Try the goal at the current index.
            except:
                 currGoalArgs = goals[currGoal]
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
        # if wasCut:
        #     wasCut = False
        #     break


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
        if isinstance(arg, ListPL):
            result.extend(findVars(arg.value))
        if isinstance(arg, Var) and arg.name[0] != "_":
            if isinstance(arg.value, list):
                arg.value = flatten(arg.value)
            result.append(arg)
    return result



# #### Built-in Features ####

# The Prolog is/2 predicate, with a different name because "is" already exists in Python.
is_ = Predicate("is_")
+is_("Q", "Q")

# fail/0.
fail = Predicate("failPredicate")

write = Predicate("write")

member = Predicate("member")
+member("X", ["X", "|", "_"])
member("X", ["_", "|", "T"]) >> [member("X", "T")]

append = Predicate("append")
+append([], "Y", "Y")
append(["X", "|", "L1"], "L2", ["X", "|", "L3"]) >> [append("L1", "L2", "L3")]

# cut (!) predicate.
cut = Predicate("cut")

# # once/1

setEqual = Predicate("setEqual")
notEqual = Predicate("notEqual")

# # # Use this for all comparisons, such as >, =, 
# # compare = Predicate("compare")

# evaluate = Predicate("evaluate")

# (\+)/1 predicate.
not_ = Predicate("isNot")

not_("A") >> ["A", cut(), fail()]
+not_("_")

# </2 predicate.
lt_ = Predicate("less than")
le_ = Predicate("less than or equal")
gt_ = Predicate("greater than")
ge_ = Predicate("greater than or equal")


between = Predicate("between")
between("N", "M", "K") >> [le_("N", "M"), setEqual("K", "N")]
between("N", "M", "K") >> [lt_("N", "M"), is_("N1", "N" |plus| 1), between("N1", "M", "K")]






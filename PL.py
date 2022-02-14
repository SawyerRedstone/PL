# The PL Module offers Prolog functionality for Python programmers.
# Created by Sawyer Redstone.

def solve(goal = []):
    newGoal = stringsToTerms(goal)
    for success in tryGoal(Goal(newGoal)):
        yield success


# This will take a list, for example [just_ate, "A", "C"], and convert all the strings to Terms.
def stringsToTerms(oldList, memo = {}):     # Memo is a dict of terms already created
    newList = []
    for word in oldList:
        # Represent duplicate strings as the same Term.
        if str(word) in memo:
            nextWord = memo[word]
        # If the word is a predicate or list, don't change it.
        elif isinstance(word, Predicate):
            nextWord = word
        elif isinstance(word, list):
            recursed = stringsToTerms(word, memo)
            memo[str(word)] = ListPL(recursed)
            nextWord = memo[str(word)]
        # Anything with a space or digit must be Math.
        elif ' ' in word or word.isdigit():
            parts = word.split()
            parts = [memo[part] if part in memo else part for part in parts]
            memo[word] = Math(word, parts)
            nextWord = memo[word]
        # Otherwise, if the first letter is uppercase, it is a Var.
        # elif word[0].isupper():     
        elif word[0].isupper() or word[0] == "_":    # Does _ work???
            memo[word] = Var(word)
            nextWord = memo[word]
        # All other strings are Consts.
        else:                       
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
    def add(self, args = [], goals = []):
        """
        'add' is used to add clauses (fact or rules) for a predicate.

        It is called with a list of the args that appear in the head of the clause being added,
        followed (optionally) by a list of goals that, if followed, can satisfy the query.
        """
        if len(args) in self.alternatives:
            self.alternatives[len(args)].append(Alt(args, goals))
        else:
            self.alternatives[len(args)] = [Alt(args, goals)]



# Goals must be completed in order to satisfy a query.
class Goal():
    def __init__(self, info):
        self.pred = info[0]               # The predicate that is being queried.
        self.args = info[1:]          # Create a list of the goal's arguments.
    def __str__(self):
        return "goalPred: " + self.pred.name + "\nGoalArgs: " + str(self.args) + "\n"


# Alts are individual alternatives that were added to a predicate.
class Alt():
    def __init__(self, args, goals): 
        self.args = args  
        self.goals = goals
    def __str__(self):
        return "altArgs: " + str(self.args) + "\naltGoals: " + str(self.goals) + "\n"
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))


# Variables and Constants are Terms.
class Term():
    def __init__(self, name, value):
        self.name = name
        # self.value = str(value)
        self.value = value
        self.children = []                  # The children are the variables that will change if this term has a value.
    def __eq__(self, other):
        if isinstance(other, Term):
            return self.value == other.value    # This is used to compare terms.
        return self.value == other
    def __bool__(self):
        return self.value != "Undefined"    # A term is false it if has no value.
    def __repr__(self):
        return repr(self.name + " = " + str(self.value))    
    def __hash__(self):
        return hash(repr(self))
    
        
class Var(Term):
    def __init__(self, name):
        super().__init__(name = name, value = "Undefined")    # Initialize the Var.
    def __str__(self):
        return str(self.value)


class Const(Term):  # A constant, aka an atom.
    def __init__(self, value):
        super().__init__(name = "Const", value = value)
    def __str__(self):
        return self.name + " = " + str(self.value)  # This is used to print the term.
    

class Math(Term):        # This is a number or mathematical expression.
    def __init__(self, name, terms):
        self.terms = terms
        super().__init__(name = name, value = "Undefined")
    def __str__(self):
        try:
            # First turn each term into its value form.
            self.terms = [str(term) for term in self.terms]
            # Then evalute and return the results.
            result = float(eval("".join(self.terms)))
            return ('%f' % result).rstrip('0').rstrip('.')  # Strip trailing 0s.
        # Catch if the user typed math that makes no sense, such as adding "3 + *".
        except:
            raise Exception("Your equation \"" + self.name + "\" seems to have an error in it.") from None

# class ListPL(Term):
#     def __init__(self, lst):  # Value is a list as a string.
#         self.head = lst
#         self.tail = []
#         if '|' in lst:
#             self.head = lst[:-2]
#             self.tail = lst[-1]
#         super().__init__(name = "List", value = lst)
#     def __len__(self):
#         return len(self.value)
#     def __eq__(self, other):
#         self.head.extend(self.tail.value) == other.head.extend(other.tail.value)

# # A list is sort of a Var?
class ListPL(Term):
    def __init__(self, lst):  # Value is a list as a string.
        # This may look like [0, 1, 2] or [0, |, A].
        self.head = lst[0]
        if len(lst) == 1:       # There is only one item in the list.
            self.tail = []
        elif lst[1] == "|":     # The tail comes after the "|".
            self.tail = ListPL(lst[-1]) 
        else:                   # The rest of the list is all the tail.
            self.tail = ListPL(lst[1:])
        super().__init__(name = "List", value = self.head)
    def __len__(self):
        return len(self.value)
    def __eq__(self, other):
        self.head.extend(self.tail.value) == other.head.extend(other.tail.value)
        



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
                    # yield [arg for arg in goal.args if isinstance(arg, Var) and arg.value != "Undefined"] or True
            # Clear any args that were defined in this goal, so they may be reused for the next alt.
            for arg in goal.args:
                if isinstance(arg, Var):
                    changePath(arg, "Undefined")
    # If no predicate exists with this number of arguments, it may be a built-in predicate.
    elif goal.pred == write and len(goal.args) == 1:
            print(goal.args[0].value)
            yield True
    # After trying all alts, reset any Vars that were turned into Consts.
    goal.args = originalArgs
    yield False               # If all the alts failed, then the goal failed.


# This tries the current alternative to see if it succeeds.
def tryAlt(query, alt):
    # Memo is a dictionary of all terms in this alt.
    # This makes sure that no terms are duplicates.
    memo = {}       
    altArgs = stringsToTerms(alt.args, memo)
    altGoals = [Goal(stringsToTerms(goal, memo)) for goal in alt.goals]
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
    # # If lengths aren't equal, check if "|" in longer one. If so, Var after "|" = end of other list.
    # if len(queryArgs) != len(altArgs):
    #     shorterList = min([queryArgs, altArgs], key=len)        # Shorter list has the tail.
    #     longerList = max([queryArgs, altArgs], key=len)
    #     if "|" in shorterList:
    #         shorterList.tail.value = longerList[len(longerList) - len(shorterList):]
    #     else:
    #         return False
    # First check if they are able to unify.
    for queryArg, altArg in zip(queryArgs, altArgs):
        if isinstance(queryArg, ListPL) and isinstance(altArg, ListPL):
            shorterList = min([queryArg, altArg], key=len)        # Shorter list has the tail.
            longerList = max([queryArg, altArg], key=len)
            tryUnify(shorterList.head, longerList.value[:len(shorterList)])
            shorterList.tail.value = longerList.value[len(shorterList.head):]# Don't forget that tail might be []!! ???
            # tryUnify(queryArg.value, altArg.value)
        if queryArg and altArg and queryArg != altArg:  # If the args both have values and not equal, fail.
            return False
        # Remove the alt's previous children.
        altArg.children.clear()
    # If it reaches this point, they can be unified.
    for queryArg, altArg in zip(queryArgs, altArgs):              # Loop through the query and alt arguments.
        # Evalute args in case they have math in them.
        if isinstance(queryArg, Math):
            queryArg.value = str(eval("queryArg"))
        if isinstance(altArg, Math):
            altArg.value = str(eval("altArg"))
        # Now that they have been evaluated, check once again if they can unify.
        if queryArg and altArg and queryArg != altArg:  # If the args both have values and not equal, fail.
            return False
        altArg.children.append(queryArg)         # The children are the variables we want to find out.
        if queryArg:
            altArg.value = queryArg.value
        changePath(altArg, altArg.value)  # Set all unified terms to new value.   
    return True                                 # If it reaches this point, they can be unified.    


def changePath(arg, newValue):
    if isinstance(arg, Term):
        arg.value = newValue
        for child in arg.children:
            # if child value already is new value, maybe don't need to change child's path? Try later! ???
            changePath(child, newValue)         # Change each parent to the new value.


# Returns a list of all Vars found in a list.
def findVars(args, memo = set()):
    result = []
    for arg in args:
        if isinstance(arg, ListPL):
            result.extend(findVars(arg.value, memo))
        # elif isinstance(arg, Var) and arg not in memo:
        elif isinstance(arg, Var) and arg[0] != "_" and arg not in memo:
            memo.add(arg)
            result.append(arg)
    return result




# #### Built-in Predicates ####

# # The Prolog is/2 predicate, with a different name because "is" already exists in Python.
equals = Predicate("equals")
equals.add(["Q", "Q"])

# # fail/0. This works differently from other goals, as users do not need to type Goal(fail)
fail = Predicate("failPredicate")

# # write/1
write = Predicate("write")
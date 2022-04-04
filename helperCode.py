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
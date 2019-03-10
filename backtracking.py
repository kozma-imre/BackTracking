# bactracking function



"""
A class that we introduced to store each backtracking branch's associated copy of the data (variables, domains, ...)
The data members are the variables of the KenKen board, the domains corresponding to each variable, each variables
neighbors and the functions that represent the present constraints
"""
class Backtrack:  # todo testing with Imre
    def __init__ (self, variables, domains, neighbors, constraints):
        """Construct a backtrack problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        # the remaining consisting values domains
        self.curr_domains = None
        # self.nassigns = 0

    """Number of conflicts board[var] has with other variables."""
    def number_of_conflicting_vars (self, var, val, board):
        return count(v in board and not self.constraints(var, val, v, board[v])
                     for v in self.neighbors[var])

    def init_curr_domains (self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    # Remove value from curr_domains[var] and add it to removals list
    def remove_from_curr_domain (self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    # Make the supposition that value is in curr_domains[var] and return the remaining possible values for other vars
    def suppose (self, var, value):
        self.init_curr_domains()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    # All values that are not excluded yet for var
    def possible_values (self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    # Restore the curr_domains of the variables in removals
    def restore (self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)


# __________________ BACKTRACKING __________________
def just_backtracking (backtrack, board, assignments=0):
    print("Backtrack...")
    if len(board) == len(backtrack.variables):
        return assignments, board

    # taking first variable
    var = first_unassigned_variable(board, backtrack)
    # looping through its domain
    for value in backtrack.possible_values(var):
        # if the constraints are satisfied backtrack
        if backtrack.number_of_conflicting_vars(var, value, board) == 0:
            # backtrack.assign(var, value, board)
            board[var] = value
            assignments += 1
            assignments, result = just_backtracking(backtrack, board, assignments)
            if result is not None:
                return assignments, result

    if var in board:
        del board[var]
    return assignments, None


# __________ Optimizing algorithms ____________

def mvr (board, backtrack):
    # key the ordering criterion, int this case this is the size of the domenium
    result = []
    for var in backtrack.variables:
        if var not in board:
            result.append(var)

    #key is the criterial for the min() which use the size of domainium
    return min(result, key=lambda v: number_of_values(backtrack, v, board))

#counting the legal values of the domenium
def number_of_values (Backtrack, var, board):
    if Backtrack.curr_domains:
        return len(Backtrack.curr_domains[var])
    else:
        return count(Backtrack.number_of_conflicting_vars(var, val, board) == 0
                     for val in Backtrack.domains[var])


# AC3

# Forward checking


# ________ Helper functions __________
def first_unassigned_variable (board, backtrack):
    """The default variable order."""
    for var in backtrack.variables:
        if var not in board:
            return var

# Count the number of items in sequence
def count (seq):
    return sum(bool(x) for x in seq)

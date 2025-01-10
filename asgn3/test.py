# this code solves only solution 2



def conflicts(curr, nodes, arcs):
    #returns number of conflicts curr causes
     #calculate Y neighbors
    #changed function so that some values can be 0/not set yet and it should return remaining conflicts
    y_index = nodes.index("Y") 
    r_index = nodes.index("R") 
    g_index = nodes.index("G") 
    b_index = nodes.index("B") 
    v_index = nodes.index("V") 

    y_prod = 1
    g_sum = 0
    b_sum = 0
    v_prod = 1

    conflicts_violated = 0

    considering_y = True
    considering_g = True
    considering_b = True
    considering_v = True

    for s, e in arcs:
        if s == y_index or e == y_index:
            neighbor = e if s == y_index else s
            if curr[neighbor] == 0:
                considering_y = False
                continue
            y_prod *= curr[neighbor]
        if s == v_index or e == v_index:
            neighbor = e if s == v_index else s
            if curr[neighbor] == 0:
                considering_v = False
                continue
            v_prod *= curr[neighbor]
        if s == g_index or e == g_index:
            neighbor = e if s == g_index else s
            if curr[neighbor] == 0:
                considering_g = False
                continue
            g_sum += curr[neighbor]
            
        if s == b_index or e == b_index:
            neighbor = e if s == b_index else s
            if curr[neighbor] == 0:
                considering_b = False
                continue
            b_sum += curr[neighbor]
    
    if curr[y_index] != 0 and considering_y and curr[y_index] != y_prod % 10:
        conflicts_violated += 1
    if  curr[g_index] != 0 and considering_g and curr[g_index] != g_sum % 10:
       conflicts_violated += 1
    if  curr[v_index] != 0 and considering_v and curr[v_index] != int(str(v_prod)[0]):
        conflicts_violated += 1
    if  curr[b_index] != 0 and considering_b and curr[b_index] != int(str(b_sum)[0]):
        conflicts_violated += 1

    # only consider if a 

    return conflicts_violated

def check_solution(curr, nodes, arcs):
    # returns True if current_state is a solution to CSP, false otherwise

    # - Yellow - equals the rightmost digit of of the product of all its neighbors
    # - Green - equals the rightmost digit of the sum of all its neighbors 
    # - Blue - equals the leftmost digit of the sum of all its neighbors
    # - Violet - equals the leftmost digit of the product of all of its neighbors

    if len(curr) != len(nodes):
        return False
    
    for i in curr:
        if i < 1 or i > 9:
            return False
        
    if conflicts(curr, nodes, arcs) > 0:
        return False

    return True

#def minimum_remianing_values(curr, nodes, arcs):
    # return the index of nodes that has the minimum remaining values legal operations left

def initial_value(nodes, arcs, domain):
    curr = [0,0,0,0,0] 
    for variable in range(len(nodes)):
        best_val = 0
        least_conflicts = float("+inf")
        for value in domain:
            #print("considering", value, "for", nodes[variable])
            curr[variable] = value
            curr_conflicts = conflicts(curr, nodes, arcs)
            #print("curr is", curr)
            #print("conflicts are", curr_conflicts)
            if curr_conflicts < least_conflicts:
                least_conflicts = curr_conflicts
                best_val = value
        
        curr[variable] = best_val
    
    #print("initial state is", curr)
    return curr


def solve_csp(nodes, arcs, max_steps):
    """
    This function solves the csp using the MinConflicts Search Algorithm.

    :param nodes, a list of letters that indicates what type of node it is,
                  the index of the node in the list indicates its id
                  letters = {R, Y, G, B, V}

    :param arcs,  a list of tuples that contains two numbers, indicating the
                  IDs of the nodes the arc connects.

    :param max_steps, max number of steps to make before giving up

    returns a list of values for the solution to the CSP where the
             index of the value corresponds the value for that given node.
    """
    domain = [1,2,3,4,5,6,7,8,9]
    curr = initial_value(nodes, arcs, domain)  #empty assignment
    #print("curr is now", curr)
    variable = 0
    # you can define an ordering for nodes. in this case we will just go through nodes in the order they are presented
    for i in range(max_steps):
        if check_solution(curr, nodes, arcs):
            return curr
        #print("number of conflicts", conflicts(curr, nodes, arcs))
        # pick a random conflicted variable
        # pick a variable that is least conflicting
        # best val is first equal to current assignment
        best_val = 0
        least_conflicts = float("+inf")
        for v in domain:
            curr[variable] = v
            curr_conflicts = conflicts(curr, nodes, arcs)
            if curr_conflicts < least_conflicts:
                least_conflicts = curr_conflicts
                best_val = v
        
        curr[variable] = best_val
        #print("reset best val of", nodes[variable], "to", best_val)
        #print("curr is now", curr)
        variable = (variable + 1) % 5
    
    #returning failure
    return curr

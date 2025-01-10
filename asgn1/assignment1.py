# Githika Annapureddy
# CruzId: gannapur

# Questions: 1b how to break alphabetic tie bwtween c and goal, 
#           1c did i make the list correctly from the search tree


# YOUR ANSWERS HERE
def question1():
    """
    Description:
    [Enter a description of your reasoning for each of a through c here.]
    Draw Search Tree for Each
    a - BFS - [start, 'a', 'd', 'b', goal]
        start -> a, start -> d, a-> b, d -> goal

    b - DFS - [start, 'a', 'b', goal] OR [start, 'a', 'b', 'c', backtrack to b, goal]
        depending on what comes first alphabetically, c or goal

        let's say c comes first alphabetically
        start -> a, a -> b, b-> c, c -> goal

    c - Uniform Cost Search
        start -> 'a', start -> 'd', a -> 'b', 'b' -> 'c', 
        'b' -> goal, 'c' -> goal, 'd' -> goal]
        Uniform Cost Search found all ways to get to goal from start, 
        and found that the cheapest route has weight 6. 
    
    """
    start = 'Start'
    goal = 'Goal'
    
    a = [start, 'a', 'd', 'b', goal]
    b = [start, 'a', 'b', 'c', goal]
    c = [start, 'a', 'd', 'b', 'c', goal, 'd', goal]
    
    return a, b, c

   
# YOUR ANSWERS HERE
def question2():
    """
    Description:
    [Enter a description of your reasoning for each of a through f here.]
    a - BFS - 
        start -> a, start -> goal

    b - Uniform Cost Search
        start -> a, start -> goal, a -> b, a -> c, c-> d, c -> goal, d-> goal, b -> d
        least weight path to goal is start -> a -> c -> goal = weight of 4

    c - DFS - 
        start -> 'a' -> 'b' -> 'd' -> goal
        - don't care about weights, just go to alphabetically first node at each iteration
    d - A* Search
    e - 
    f - 
    """
    start = 'Start'
    goal = 'Goal'
       
    a = [start, 'a', goal]
    b = [start, 'a', goal, 'b', 'c', 'c', goal, goal, 'd']
    c = [start, 'a', 'b', 'd', goal]
    d = None
    e = None
    f = None
    
    return a, b, c, d, e, f


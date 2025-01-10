# Works but ANDS all conditions rather than ORing when necessary


# Import additional methods for backchaining
from production import AND, OR, NOT, PASS, FAIL, IF, THEN, match, populate, simplify, variables
from data import zookeeper_rules

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """

    a = ["(?x) is a bird"]
    print(AND(a))

    print(simplify(AND(a)))

    return
    for i in rules:
        print(i)

    #print()
    subject, hyp_consequent = hypothesis.split(' ', 1)

    def look_for_consequent(consequent):
        #print("look_for_consequent called with consequent", consequent)
        # returns list of all antecedents to the consequent
        rel_rules = []
        for rule in rules:
            c = rule.consequent()
            if c.endswith(consequent):
                ant = rule.antecedent()
                conditions = ant.conditions()
                named_conditions = [c.replace('(?x)', subject) for c in conditions]
                rel_rules.append(AND(named_conditions))
                #print(ant, "added to rel_rules")
                #print("conditions of ant are", conditions)
                for i in range(len(conditions)):
                    results = look_for_consequent(conditions[i])
                    #print("returned from look_for_consequent called with consequent", conditions[i])
                    for result in results:
                        temp = conditions + result
                        #remove that condition
                        temp.pop(i)
                        named_conditions = [c.replace('(?x)', subject) for c in temp]
                        rel_rules.append(AND(named_conditions))
                        #print(AND(temp), "added to rel_rules")
        return rel_rules
                   
    rel_rules = look_for_consequent(hyp_consequent)
    OR(rel_rules).test_matches(hypothesis)
    rel_rules.append(hypothesis)

    # before returning convert every (?x) to subject
    return OR(rel_rules)

# Uncomment this to test out your backward chainer:
x = backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')
#print("\n\n\n\n")
print(x)
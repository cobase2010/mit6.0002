###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1

def dp_make_weight(egg_weights, target_weight, memo = None):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # each egg has weight, and size which is always 1
    # total weight is taret_weight
    #print("Calling dp with target_weight:", target_weight, "memo:", memo)
    if memo == None:
        memo = {}
    result = 0
    if all(x > target_weight for x in egg_weights):
        return target_weight + 1 #if it doesn't fit, return a larger number
    elif target_weight in egg_weights: # full egg
        return 1

    # Greedy version - only works if egg_weights contains egg_weight == 1
    # elif len(egg_weights) == 1: # only egg(1) left
    #     return target_weight # just return the number of eggs in target_weight
    # elif egg_weights[-1] > target_weight: 
    #     result = dp_make_weight(egg_weights[:-1], target_weight, memo)
    # else:
    #     result = dp_make_weight(egg_weights, target_weight - egg_weights[-1], memo) +1
    # memo[(egg_weights, target_weight)] = result
    # return result

    else: # this works with more generic version where answer may not exisit in which case
        # we return target_weight +1
        min_eggs = target_weight +1 #worst_case scenario
        num_eggs = 0
        for egg_weight in egg_weights[::-1]: # testing each egg weight for the n-1 case
            if egg_weight <= target_weight:
                new_target_weight = target_weight - egg_weight
                if new_target_weight in memo:
                    # print("Found in cache: ", new_target_weight)
                    num_eggs = memo[new_target_weight] + 1
                    # found optimal, no need to continue
                    # min_eggs = num_eggs
                    #break
                else:
                    num_eggs = dp_make_weight(egg_weights, new_target_weight, memo) +1
                if num_eggs< min_eggs and num_eggs <= new_target_weight:
                    min_eggs = num_eggs
            else: #can't fit this egg inside, skip to the next egg size
                continue

            
        #print("Adding", (target_weight, min_eggs), "to memo...")
        memo[target_weight] = min_eggs
        return min_eggs

                    





# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (2, 5)
    n = 6
    print("Actual output:", dp_make_weight(egg_weights, n))

    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights =", egg_weights)
    print("n =", n)
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 5, 10, 25, 50)
    n = 199
    print("Egg weights =", egg_weights)
    print("n =", n)
    print("Expected ouput: 10 (3 * 50 + 1 * 25 + 2 * 10 + 4 * 1 = 199)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()



"""
Answer to problem B:
1. It depends on what the n is. The larger n is, the more difficulty the bruite force
    algorithm is going to be. In fact, even in DP, if I loop the egg_weights from small to large, 
    it can create recursive depth problem for large n with egg_weights of size 30.
2. Objective function is lamda x: target_weight - x. 
    Constraints: egg_weights needs to contain egg of weight 1. 
3. Counter example for greedy to not work: egg_weights = (2, 5), target_weight = 6. Greedy won't
    find answer, but actual is 3.



"""


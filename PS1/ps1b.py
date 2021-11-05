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
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    # each egg has weight, and size which is always 1
    # total weight is taret_weight
    result = 0
    if (egg_weights, target_weight) in memo:
        print("Found in cache:", (egg_weights, target_weight))
        #print(memo)
        return memo[(egg_weights, target_weight)]
    elif target_weight == 0: # no more target weights
        return 0
    elif len(egg_weights) == 1: # only egg(1) left
        return target_weight # just return the number of eggs in target_weight
    elif egg_weights[-1] > target_weight: 
        result = dp_make_weight(egg_weights[:-1], target_weight, memo)
    else:
        result = dp_make_weight(egg_weights, target_weight - egg_weights[-1], memo) +1
    memo[(egg_weights, target_weight)] = result
    return result



# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 5, 10, 25, 50)
    n = 199
    print("Egg weights = (1, 5, 10, 25, 50)")
    print("n = 199")
    print("Expected ouput: 10 (3 * 50 + 1 * 25 + 2 * 10 + 4 * 1 = 199)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

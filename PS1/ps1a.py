###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # Your code here
    dict = {}
    print("Loading cow data from file...")
    # inFile: file
    inFile = open(filename, 'r')
    # line: string
    for line in inFile:
        # cowlit: list of stringss
        cowlist = line.split(',')
        dict[cowlist[0]] = int(cowlist[1])

    print("  ", len(dict), "cows loaded.")
    inFile.close()
    return dict
    pass

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Your code here
    sorted_cows = [k for (k, v) in sorted(cows.items(), key=lambda x: x[1], reverse = True)]
    result = []
    
    while (len(sorted_cows) > 0):
        names = []
        totalWeight = 0
        for i in sorted_cows:
            if totalWeight+cows[i] <= limit:  # can fit in the transport
                totalWeight += cows[i]
                names.append(i)
        if (len(names) == 0):
            # no more cows to fit 
            break
        else:
            result.append(names)
            for name in names:
                sorted_cows.remove(name)
    return result


    return sorted_cows
    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Your code here
    count = 0
    dict = {}   # use a dictionary to map partition size to partitions
                # format: len->list of partitions of length len
    for partition in get_partitions(cows.keys()):
    # for partition in get_partitions(['one','two','three']):
            if len(partition) in dict:
                dict[len(partition)].append(partition)
            else:
                dict[len(partition)] = [partition]

            count += 1
    # print(count, "partitions generated")
    # print(dict[1])

    for i in range(1, len(cows.keys())+1):
        # testing each 1 trip, 2 trips, etc.
        
        for trips in dict[i]:
            
            valid = True
            for trip in trips:
                cost = 0
                for cow in trip:
                    cost += cows[cow]
                if cost > limit: # broke it
                    valid = False
            if valid:
                #found a good trips
                return trips
    return [[]] #no trips found

            


        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # Your code here
    filename = 'ps1_cow_data.txt'
    # testing load_file
    dict = load_cows(filename)
    print(dict)
    print("Total weight:", sum(dict.values()))
    start = time.time_ns()
    transport_list = greedy_cow_transport(dict, 10)
    end = time.time_ns()
    print("Number of trips found by greedy_cow", len(transport_list))
    print("greedy_cow_transport took:", "{:.4f}".format((end - start)/1000000), "ms.")
    print(transport_list)

    start = time.time_ns()

    transport_list = brute_force_cow_transport(dict, 10)    
    end = time.time_ns()
    print("Number of trips found by brute_force", len(transport_list))
    print("brute_force_transport took:", "{:.4f}".format((end - start)/1000000), "ms.")
    print(transport_list)

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    compare_cow_transport_algorithms()

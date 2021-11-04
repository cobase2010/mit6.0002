# 6.00
# Problem Set 5 Test Suite
import unittest
import string
from ps1a import *

class ProblemSet1(unittest.TestCase):
    def setUp(self):
        print('\n')
        pass

    def testLoadCow(self):
        dict = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3, 'Milkshake': 2, 'Millie': 5, 'Lola': 2, 'Florence': 2, 'Henrietta': 9}
        filename = 'ps1_cow_data.txt'
        # testing load_file
        dict2 = load_cows(filename)
        self.assertEqual(dict, dict2)

        dict = {"Miss Moo-dy":3, "Milkshake":4, "Lotus":10, "Miss Bella":2, "Horns":9, "Betsy":5, "Rose":3, "Dottie":6}
        filename = 'ps1_cow_data_2.txt'
        # testing load_file
        dict2 = load_cows(filename)
        self.assertEqual(dict, dict2)

    def testGreedyCowTransport(self):
        res = [['Betsy'], ['Henrietta'], ['Herman', 'Maggie'], ['Oreo', 'Moo Moo'], ['Millie', 'Milkshake', 'Lola'], ['Florence']]
        filename = 'ps1_cow_data.txt'
        # testing load_file
        dict = load_cows(filename)
        print(dict)
        start = time.time_ns()
        transport_list = greedy_cow_transport(dict, 10)
        end = time.time_ns()
        print("greedy_cow_transport took:", "{:.0f}".format(end - start), "ns.")
        print(transport_list)
        self.assertEqual(transport_list, res)

    def testBruteForceTransport(self):
        res = 5
        filename = 'ps1_cow_data.txt'
        # testing load_file
        dict = load_cows(filename)
        #print(dict)
        # for partition in get_partitions([1,2,3]):
        #     print(partition)
        start = time.time_ns()

        transport_list = brute_force_cow_transport(dict, 10)    
        end = time.time_ns()
        print("brute_force_transport took:", "{:.0f}".format(end - start), "ns.")
        print(transport_list)

        self.assertEqual(res, len(transport_list))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProblemSet1))
    unittest.TextTestRunner(verbosity=2).run(suite)

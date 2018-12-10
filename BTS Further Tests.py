from random import shuffle
import csv
from multiprocessing import Process
from multiprocessing import Manager
import numpy as np
import math
import itertools
start = 1
end = 10
trail = 500
step = 2
threads_count = 8

class Tree():

    def __init__(self,value = None,left = None,right = None): # Node object
        self.value = value
        self.left = left
        self.right = right

    def insert(self,x): # a wrapper for the insertion function
        self.rec_insert(x)

    def rec_insert(current,x):
        if current == None: # put the calue at an empty branch
            return Tree(x,None,None)
        elif current.value > x:
            current.left = Tree.rec_insert(current.left,x) # go to the left branch
        else:
            current.right = Tree.rec_insert(current.right,x) # go to the right branch
        return current

    def height(self,tree=None):
        if tree == None: # represents the empty node
            return 0
        return max(self.height(tree.left),self.height(tree.right)) + 1


def generate_random_array(n): # generate a pseudo random array using built-in shuffle()
    array = [i for i in range (n)]
    shuffle(array)
    return array

def build_tree(arr): # build a tree from an array
    tree = Tree(arr[0], None, None)
    for i in range (1,len(arr)):
        tree.insert(arr[i])
    return tree

def mainThread(start, end, results):
    #esults = []   # the results container

    # Trails and recording data
    #print("Generating results.....")
    for n in range(start, end, step):
        height_sum = 0
        for t in range(trail):
            arr = generate_random_array(n)
            tree = build_tree(arr)
            height_sum = height_sum + tree.height(tree)
        results[n] = (height_sum / trail)
        #print("n = %4d, h = %2.3f" % (results[-1][0], results[-1][1]))  # print the current result to the console

    return results

def quadratic_solver(a,b,c):
    d = (b ** 2) - (4 * a * c)
    sol = (-b + math.sqrt(d)) / (2 * a)
    return sol

def determine_steps_for_loop(total_operations):
    #print (total_operations)
    individual_operation = total_operations/threads_count
    prvEnd = 0
    tabs = [1]
    for i in range(threads_count):
        nextTab = int(quadratic_solver(1,1,-individual_operation*2-prvEnd*(prvEnd+1)))
        tabs.append(nextTab)
        prvEnd = nextTab
    tabs[-1] = end # make sure the last element is covered
    return tabs


def serilizer(f,args_in_array):
    processes = []
    for i in range(threads_count):
        p = Process(target=f,args = args_in_array[i])
        processes.append(p)
    return processes

def determine_steps_parallelit(total_operations):
    return [2,3,4,5,6,7,8,9]
    #return [20,30,35,38,39,40,41,42]

def parallelit(end,results):
    start = 1
    l = [i for i in range(start,end+1)]
    perms = list(itertools.permutations(l))
    permList = []
    for p in perms:
        permList.append(list(p))
    #print("permutation list", permList)
    key = len(p)
    result = []
    for p in permList:
        tree = build_tree(p)
        result.append(tree.height(tree))
    print(sum(result)/len(permList))
    result_count = [0 for x in range (30)]
    for item in result:
        result_count[item] = result_count[item]+1
    readable_list = []
    for i in range (30):
        if result_count[i]!=0:
            readable_list.append([i,result_count[i]])
    results[key] = readable_list

def main():
    manager = Manager()
    results = manager.dict()
    args_array = []
    tabs = determine_steps_parallelit(((end * (end + 1) - start * (start + 1)) / 2))
    for i in range (threads_count):
        args_array.append([tabs[i],results])
    processes = serilizer(parallelit, args_array)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    #print(results)
    for i in range (2,10):
        sum = 0
        sum_num = 0
        for pair in results[i]:
            sum += pair[0]*pair[1]
            sum_num += pair[1]
        print(results[i],"average is for tree containing", i,"nodes:",sum,"/",sum_num)

def parallel_main():
    print("n is the number of vertices in the Binary Search Tree \nh is the corresponding average height of trail randomly generated sample\n")
    #results = [["number of nodes", "height"]]
    manager = Manager()
    results = manager.dict()

    tabs = determine_steps_for_loop(((end*(end+1)-start*(start+1))/2))
    print(tabs[1:])

    args_array = []
    for i in range (threads_count):
        args_array.append([tabs[i],tabs[i+1],results])
    #print(args_array)
    processes = serilizer(mainThread,args_array)

    for p in processes:
        p.start()
    for p in processes:
        p.join()
    converted_results = [[],[]]
    converted_results[0] = (results.keys())
    converted_results[1] = (results.values())
    results = []

    for i in range (len(converted_results[0])):
        results.append([converted_results[0][i],converted_results[1][i]])
    results = np.array(results)
    results.sort(axis=0)
    with open("results.csv","w+") as csv_file: # write result to a csv file
        writer = csv.writer(csv_file)
        writer.writerows(results)

#main()



def further():
    results = [["number of nodes", "height"]]  # the results container
    trail = 500

    # Trails and recording data
    print("Generating results.....")
    # for n in range(100, 1001, 100):
    n = 10
    heights = []
    for t in range(trail):
        arr = generate_random_array(n)
        tree = build_tree(arr)
        heights.append([tree.height(tree)])
    with open("further results.csv", "w+") as csv_file:  # write result to a csv file
        writer = csv.writer(csv_file)
        writer.writerows(heights)
#further()
def test():
    tree = build_tree([8,4,2,1,3,6,5,7,12,10,9,11,14,13,15])
    print(tree.height(tree))
main()
# Sample Results:
# n =  100, h = 13.326
# n =  200, h = 15.828
# n =  300, h = 17.442
# n =  400, h = 18.476
# n =  trail, h = 19.476
# n =  600, h = 20.132
# n =  700, h = 20.632
# n =  800, h = 21.164
# n =  900, h = 21.538
# n = 1000, h = 22.102

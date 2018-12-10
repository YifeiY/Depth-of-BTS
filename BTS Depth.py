from random import shuffle
import csv


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

def main():
    print("n is the number of vertices in the Binary Search Tree \nh is the corresponding average height of 500 randomly generated sample\n")
    results = [["number of nodes","height"]] # the results container
    trail = 500

    #Trails and recording data
    print("Generating results.....")
    for n in range (100, 1001, 100):
        height_sum = 0
        for t in range (trail):
            arr = generate_random_array(n)
            tree = build_tree(arr)
            height_sum = height_sum + tree.height(tree)
        results.append([n,height_sum/500])
        print("n = %4d, h = %2.3f" % (results[-1][0], results[-1][1])) # print the current result to the console


    with open("results.csv","w+") as csv_file: # write result to a csv file
        writer = csv.writer(csv_file)
        writer.writerows(results)

main()
# Sample Results:
# n =  100, h = 13.326
# n =  200, h = 15.828
# n =  300, h = 17.442
# n =  400, h = 18.476
# n =  500, h = 19.476
# n =  600, h = 20.132
# n =  700, h = 20.632
# n =  800, h = 21.164
# n =  900, h = 21.538
# n = 1000, h = 22.102

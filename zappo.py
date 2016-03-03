# Author: Elliott Ploutz
# Completed for the Zappos 2016 challenge.

import math
import heapq # PriorityQueue

#####################################################################
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
#####################################################################

valueSet = set()

class node(object):
    def __init__(self):
        self.move = ""
        self.value = 0
        self.depth = 0
        self.parent = None

def addNode(move, val, depth, parnt):
    nd = node()
    nd.move = move
    nd.value = val
    nd.depth = depth
    nd.parent = parnt
    return nd

def subsequenceAdd(numString):
    subSeq = []
    i = len(numString)
    j = 0
    # Find all subsequences
    while(j != len(numString)):
        while(j < i):
            subSeq.append(int(numString[j:i]))
            i = i-1
        j = j+1
        i = len(numString)
    # Add them to num
    num = int(numString)
    subSeqAdd = []
    for i in range(len(subSeq)):
        subSeqAdd.append(["Added " + str(subSeq[i]), num + subSeq[i]])
    return subSeqAdd

def splitMult(numString):
    if (len(numString) == 1):
        return []
    splits = []
    i = 1
    while(i != len(numString)):
        a = numString[:i]
        b = numString[i:]
        splits.append(["Multiplied "+a+" and "+b, int(a) * int(b)])
        i = i+1
    return splits

# Little Biiitsss - Rick and Morty
def swapLilBits(numString):
    num = int(numString)
    # Bit masks to isolate swapping bits
    leadMask = 2
    trailMask = 1
    # Sequence of swap
    seq = []
    while(leadMask <= num):
        leadIsolate = num & leadMask
        trailIsolate = num & trailMask
        # Significance of bit Swapped
        significance = str(int(math.log2(leadMask)))
        # Do swap because they're different, else it's the same, no swap.
        if (leadIsolate != 0 and trailIsolate == 0):
            swap = num | (int(leadIsolate/2))    # swap trailing bit
            swap = swap ^ leadIsolate        # definite 0
            seq.append(["Swapped bits "+str(int(significance)-1)+" and " + significance, swap])
        if (leadIsolate == 0 and trailIsolate != 0):
            swap = num | (trailIsolate*2)    # swap leading bit
            swap = swap ^ trailIsolate       # definite 0
            seq.append(["Swapped bits "+str(int(significance)-1)+" and " + significance, swap])
        leadMask = leadMask * 2
        trailMask = trailMask * 2
    # Final swap with most significant 0
    significance = str(int(math.log2(leadMask)))
    leadIsolate = num & leadMask
    trailIsolate = num & trailMask
    swap = num | (trailIsolate*2)    # swap leading bit
    swap = swap ^ trailIsolate       # definite 0
    seq.append(["Swapped bits "+str(int(significance)-1)+" and " + significance, swap])
    return seq
#See also int.bit_length() returns the number of bits necessary to represent an integer in binary, excluding the sign and leading zeros

def printChain(node, length):
    if (None != node):
        printChain(node.parent, length+1)
        print(node.move)
        if (node.parent != None):
            print("Value: " + str(node.value))
    else:
        print('')
        print("Chain length: " + str(length))
        print('')

'''
Best-First Search
node = state, top(heuristic), h
Algorithm (tree):
    1) Put start state m open; calculate h(IS);
    2) If open = 0, then fail
        Else remove from open with smallest h-value (call it n)
        and put it on closed
    3) Expand n; set back pointers of successors to in;
        calculate h-values; put them on open;
    4) If any successor is a goal then succeed
        Else go to 2.
'''
def bestFirstSearch(openQ, finalV):
    # Continue until solution is found or open queue is empty.
    global valueSet
    while([] != openQ._queue):
        #print("Going...")
        node = openQ.pop()
        # Expand children of current node and put on openQ.
        currValue = str(node.value)
        seqAdd = subsequenceAdd(currValue)
        seqMult = splitMult(currValue)
        seqBits = swapLilBits(currValue)
        allOperations = seqAdd + seqMult + seqBits
        for i in range(len(allOperations)):
            # Solution found
            nd = addNode(allOperations[i][0], allOperations[i][1], node.depth+1, node)
            if ((allOperations[i][1] - finalV) == 0):
                return printChain(nd, 0)
            if (nd.value not in valueSet):
                openQ.push(nd, 0) #(abs(allOperations[i][1]-finalV)) + nd.depth)
            valueSet.add(nd.value)
    print("Failure! No solution found.")

def main():
    # 5, 25, 6
    f = open("real3.txt", 'r')
    fSplit = f.read().split()
    initialV = fSplit[0]
    finalV = int(fSplit[1])

    priorityQ = PriorityQueue()
    root = addNode("Initial Value: " + initialV, int(initialV), 0, None)
    priorityQ.push(root, abs(int(initialV) - finalV))
    bestFirstSearch(priorityQ, finalV)
    f.close()

# stop building tree when it gets bigger than num2

if __name__ == "__main__":
    main()

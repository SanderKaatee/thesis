import itertools 
import random
import sys
from timeit import default_timer as timer

from collections import deque


class BAFUnit:
    def __init__(self):
        self.support_nodes = []    # list of tuples (a, b)
        self.marked_nodes = []

    def add_support_node(self, a, b):
        self.support_nodes.append((a, b))

    def remove_support_node(self, a, b):
        self.support_nodes.remove((a, b))
    
    def add_marked_node(self, a):
        self.marked_nodes.append(a)

    def remove_marked_node(self, a):
        self.marked_nodes.remove(a)
    
    def is_node_marked(self,a):
        return a in self.marked_nodes
    
    def support_node_length(self):
        return len(self.support_nodes)
        

    def get_observed_actions(self):
        return [node[1] for node in self.support_nodes]

def extract_feature_values(observation, length):
    feature_values = []
    for i, obs in enumerate(observation):
        feature_values.append((i, obs))

    # # create all combinations up to length 'length'
    # combs = []
    # for i in range(1, len(feature_values)+1): 
    #     for subset in itertools.combinations(feature_values, i):
    #             if i <= length:
    #                 combs.append(subset)
    return feature_values

def AABL(observation, BAF, length, BRB):
    combs = extract_feature_values(observation, length)
    predicted_behaviour = []
    SN = BAF.support_nodes
    for sn in SN:
        for comb in combs: 
            if sn[0]==comb:
                predicted_behaviour.append(sn[1])
    if predicted_behaviour:
        action = predicted_behaviour[0]
        # print("didnt make a random action", action)

    else:
        action = random.randint(0,8)
    
    should_Increment_L = update_BAF(BAF, BRB, combs)
    # while(should_Increment_L):
    #     length += 1
    #     combs = extract_feature_values(observation, length)
    #     should_Increment_L = update_BAF(BAF, BRB, combs)
    return action, length

def update_BAF(BAF, BRB, combs):
    SN = BAF.support_nodes
    should_Increment_L = True

    for comb in combs:
        add_support = True
        for sn in SN:
            if sn[0]==comb:
                add_support = False
                if sn[1] != BRB:
                    BAF.add_marked_node(comb)
                    BAF.remove_support_node(sn[0],sn[1])
        
        if not BAF.is_node_marked(comb):
            should_Increment_L = False
            if add_support == True:
                BAF.add_support_node(comb, BRB)
    return should_Increment_L

def generate_table():
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black', 'white', 'cyan', 'magenta', 'olive', 'navy', 'teal', 'maroon', 'coral', 'gold', 'silver']
    concepts = ['ball', 'box', 'person', 'car', 'tree', 'book', 'computer', 'phone', 'dog', 'cat']
    combinations = list(itertools.product(colors, concepts))
    combinations.append(('none', 'none'))

    recovery_behaviors = ['push', 'alt', 'ask', 'cont']

    random_list = [random.choice(recovery_behaviors) for i in range(len(combinations))]
    brb_table = {}

    for i, item in enumerate(combinations):
        brb_table[item] = random_list[i]
    
    return brb_table

def generate_game(table):
    locations = []
    for i in range(100):
        locations.append(random.choice(list(table.keys())))
    
    BRB = table[locations[4]]

    return locations, BRB

# @profile
def main():
    start_time = timer()
    length = 1
    table = generate_table()
    BAF = BAFUnit()
    history = deque(maxlen=200)


    for i in range(2000):
        locations, BRB = generate_game(table)
        action, length = AABL(locations, BAF, length, BRB)
        
        history.append(action == BRB)
        percentage = history.count(True) / len(history) * 100
        baf_length = BAF.support_node_length()
        print('BAFLENGTH %d Percentage correct %.2f Iterations %d Length %d\r' % (baf_length, percentage,i, length), end="")

    print("")
    print("done")
    print("final percentage", percentage)
    print(f"Total Process Time = {timer() - start_time}")


if __name__ == '__main__':
    main()
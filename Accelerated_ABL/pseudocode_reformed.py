import gym
import itertools 
import random
import sys
from collections import deque
from collections import Counter


class BAFUnit:
    def __init__(self):
        self.support_nodes = []     # list of tuples (a, b)
        self.marked_nodes = []
        self.length = 1
        self.previous_best_recoveries = []

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

    def extract_feature_values(self, observation):
        feature_values = []
        for i, obs in enumerate(observation):
                feature_values.append(obs[0])
                feature_values.append(obs[1])
        
        combs = feature_values
        # create all combinations up to length 'length'
        combs = []
        for i in range(1, len(feature_values)+1): 
            for subset in itertools.combinations(feature_values, i):
                    print(subset)
                    if i == self.length:
                        combs.append(subset)
                        print(subset)
                        # input("waiting...")
        return combs

    def AABL(self, observation, BRB):
        if len(observation) == 6:
            observation = observation[0]
        else:
            observation = [observation[0], observation[1]]

        self.previous_best_recoveries.append(BRB)
        
        combs = self.extract_feature_values(observation)
        predicted_behaviour = []
        SN = self.support_nodes
        for sn in SN:
            for comb in combs: 
                if sn[0]==comb:
                    predicted_behaviour.append(sn[1])
        if predicted_behaviour:
            if len(predicted_behaviour) == 1:
                action = predicted_behaviour[0]
            else:
                action = random.choice(predicted_behaviour)
        elif not self.previous_best_recoveries:
            counter = Counter(self.previous_best_recoveries)
            action = counter.most_common()
        else:
            action = ''
          
        should_Increment_L = self.update_BAF(BRB, combs)
        while(should_Increment_L and self.length <= 2):
            self.length += 1
            combs = self.extract_feature_values(observation)
            should_Increment_L = self.update_BAF(BRB, combs)

        return action

    def update_BAF(self, BRB, combs):
        # updating support relations
        SN = self.support_nodes
        should_Increment_L = True
        for comb in combs:
            add_support = True
            for sn in SN:
                if sn[0]==comb:
                    add_support = False
                    if sn[1] != BRB:
                        self.add_marked_node(comb)
                        self.remove_support_node(sn[0],sn[1])
            
            if not self.is_node_marked(comb):
                should_Increment_L = False
                if add_support == True:
                    self.add_support_node(comb, BRB)
        return should_Increment_L
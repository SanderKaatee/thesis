import gym
import itertools 
import random
import sys
from tictactoe_env import tictactoeEnv
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
    # feature values are [location, color] where 0 = empty, 1 is nought and 2 is cross
    feature_values = []
    for i in range(3):
        for j in range(3):
            feature_values.append([i*3 + j, observation[i,j]])

    # create all combinations up to length 'length'
    combs = []
    for i in range(1, len(feature_values)+1): 
        for subset in itertools.combinations(feature_values, i):
                if i <= length:
                    combs.append(subset)
    return combs

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
    while(should_Increment_L):
        length += 1
        combs = extract_feature_values(observation, length)
        should_Increment_L = update_BAF(BAF, BRB, combs)
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
            
def make_random_move(color, env):
    while True:
        # Generate a random row and column
        action = random.randint(0, 8)
        try:
            # Try to make the move
            state, reward, done, info = env.step((action, color))
            # print((color,action))
            return state, reward, done, action
        except ValueError as e:
            # If the move is invalid, try again
            continue

def play_game(actions, step_fn=input):
    env = tictactoeEnv(small=-1, large=10)
    env.reset()
    BAF = BAFUnit()

    # Play actions in action profile
    for action in actions:
        state, reward, done, info = env.step(action)
        print(env.render())
    return env

def generate_game():
    env = tictactoeEnv(small=-1, large=10)
    env.reset()
    done = False
    player = 1
    while(True):
        player = (player + 1) % 2
        state, reward, done, action = make_random_move(player+1, env)
        if done == True:
            if player == 0 and reward == 9:
                state, _, _, _ = env.step((action,0))
                break
            else:
                env.reset()
    return state, action

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

BAF = BAFUnit()
history = deque(maxlen=200)
length = 1
i = 0

while(True):
    i += 1
    env = tictactoeEnv(small=-1, large=10)
    env.reset()
    state, BRB = generate_game()
    env.load_state(state)
    action, length = AABL(state, BAF, length, BRB)
    history.append(action == BRB)
    percentage = history.count(True) / len(history) * 100
    # printProgressBar(percentage, 100, prefix = 'Progress:', suffix = 'Correct', length = 50)
    baf_length = BAF.support_node_length()
    print('BAFLENGTH %d Percentage correct %.2f Iterations %d Length %d\r' % (baf_length, percentage,i, length), end="")
    if percentage==100:
        print("")
        quit()



import numpy as np
import random

class TabularQLearning:
    def __init__(self, location, color, concept, actions, learning_rate=1, exploration_rate=0):
        self.location = location
        self.color = color
        self.concept = concept
        self.actions = actions
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((len(location), len(color), len(concept), len(actions)))

        self.location_index = {loc: i for i, loc in enumerate(location)}
        self.color_index = {col: i for i, col in enumerate(color)}
        self.concept_index = {con: i for i, con in enumerate(concept)}
        self.action_index = {act: i for i, act in enumerate(actions)}

    def get_state_index(self, state):
        loc_i = self.location_index[state[0]]
        col_i = self.color_index[state[1]]
        con_i = self.concept_index[state[2]]
        return (loc_i, col_i, con_i)

    def choose_action(self, states):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        
        max_action_value = 0
        actions_with_max_value = [random.choice(self.actions)]

        for i, obstacle in enumerate(states):
            state = [i, obstacle[0], obstacle[1]]
            state_index = self.get_state_index(state)
            action_values = self.q_table[state_index]
            
            if np.max(action_values) > max_action_value:
                max_action_value = np.max(action_values)
                actions_with_max_value = [action for action, value in zip(self.actions, action_values) if value == max_action_value]
        
        return random.choice(actions_with_max_value)

    def update_q_table(self, states, action, reward):
        for i, obstacle in enumerate(states):
            state = [i, obstacle[0], obstacle[1]]
            state_index = self.get_state_index(state)

            old_value = self.q_table[state_index + (self.action_index[action],)]

            updated_value = old_value + self.learning_rate * reward
            self.q_table[state_index + (self.action_index[action],)] = updated_value
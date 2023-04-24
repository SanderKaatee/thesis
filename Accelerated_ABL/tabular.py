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

    def get_state_index(self, states):
        for i, state in enumerate(states):
            loc_i = self.location_index[i]
            col_i = self.color_index[state[0]]
            con_i = self.concept_index[state[1]]
        return (loc_i, col_i, con_i)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        
        state_index = self.get_state_index(state)
        action_values = self.q_table[state_index]
        max_action_value = np.max(action_values)
        
        actions_with_max_value = [action for action, value in zip(self.actions, action_values) if value == max_action_value]
        
        return random.choice(actions_with_max_value)

    def update_q_table(self, state, action, reward):
        state_index = self.get_state_index(state)

        old_value = self.q_table[state_index + (self.action_index[action],)]

        updated_value = old_value + self.learning_rate * reward
        self.q_table[state_index + (self.action_index[action],)] = updated_value
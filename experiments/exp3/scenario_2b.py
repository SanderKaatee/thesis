import numpy as np
import random
from collections import Counter


class ScenarioGenerator:
    colors = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow'}
    concepts = {0: 'ball', 1: 'box', 2: 'person'}
    recovery_behaviors = {0: 'push', 1: 'ask', 2: 'alt', 3: 'continue'}
    def __init__(self, scenario_type='first'):
        if scenario_type == 'first':
            self.scenario_length = 6
        self.scenario = []
        self.best_recovery_behavior = ""
        self.ruleset = self.generate_ruleset()

    def generate_ruleset(self):
        ruleset = {}
        rb_copy = list(self.recovery_behaviors.values())
        for concept in self.concepts.values():
            rule = random.sample(rb_copy, k=1)[0]
            rb_copy.remove(rule)
            ruleset[concept] = rule
        return ruleset

    def generate_scenario(self):
        new_scenario = []
        colors_copy = list(self.colors.values())
        red_occurred = False
        
        for _ in range(self.scenario_length):
            color = random.choice(colors_copy)
            if color == 'red':
                colors_copy.remove(color)
            concept = random.choice(list(self.concepts.values()))
            new_scenario.append([color, concept])
        self.scenario = new_scenario
        self.best_recovery_behavior = self.determine_recovery()
    
    def determine_recovery(self):
        red_objects = [obj[1] for obj in self.scenario if obj[0] == 'red']
        if not red_objects:
            return 'continue'
        else:
            red_object_counts = Counter(red_objects)
            most_common_red_object = red_object_counts.most_common(1)[0][0]
            for concept, rule in self.ruleset.items():
                if concept == most_common_red_object:
                    return rule

    def scenario_to_numerical(self):
        numerical = []
        for sen in self.scenario:
            if sen[0] != "Noc":
                numerical.append(list(self.colors.keys())[list(self.colors.values()).index(sen[0])])
                numerical.append(list(self.concepts.keys())[list(self.concepts.values()).index(sen[1])])
            else:
                numerical.append(5)
                numerical.append(5)
        return numerical

    def recovery_behavior_to_numerical(self):
        numerical = list(self.recovery_behaviors.keys())[list(self.recovery_behaviors.values()).index(self.best_recovery_behavior)]
        return numerical
    
    def recovery_behavior_to_numerical_with_arg(self, recovery_behavior):
        numerical = list(self.recovery_behaviors.keys())[list(self.recovery_behaviors.values()).index(recovery_behavior)]
        return numerical

    def numerical_to_recovery_behavior(self, number):
        recovery_behavior = self.recovery_behaviors[number]
        return recovery_behavior

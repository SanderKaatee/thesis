import numpy as np

class ScenarioGenerator:
    colors = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow'}
    concepts = {0: 'ball', 1: 'box', 2: 'person'}
    recovery_behaviors = {0: 'push', 1: 'ask', 2: 'alt', 3: 'continue'}
    

    scenarios = [
        [["red","ball"]],
        [["red","box"]],
        [["red","person"]],
        [["green","ball"]],
        [["green","box"]],
        [["green","person"]],
        [["blue","ball"]],
        [["blue","box"]],
        [["blue","person"]],
        [["yellow","ball"]],
        [["yellow","box"]],
        [["yellow","person"]],
        [["Noc","Noc"]],
    ]

    BRBs = [
        "push",
        "alt",
        "ask",
        "push",
        "alt",
        "ask",
        "push",
        "alt",
        "alt",
        "push",
        "alt",
        "ask",
        "continue",
    ]

    def __init__(self):
        self.scenario = []
        self.best_recovery_behavior = ""


    def generate_scenario(self):
        self.scenario = self.scenarios[0]
        self.best_recovery_behavior = self.BRBs[0]
        self.scenarios.pop(0)
        self.BRBs.pop(0)
        

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
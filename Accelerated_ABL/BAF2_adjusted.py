import itertools
import numpy as np
import operator
import ast


class BAF2:
    gen = [0]

    def __init__(self, scenario, gen):
        self.gen[0] = gen
        self.combination_feature_weights = {}
        self.recovery_behaviors = []
        self.current_best_recovery_behavior = "Nothing"
        self.num_features_to_consider = 1

        self.num_of_columns = len(scenario)
        self.important_columns = np.arange(self.num_of_columns)

    def compute_combination_feature_weights(self, best_recovery_behavior_idx, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        should_change = False
        numerical_scenario = np.array(self.gen[0].scenario_to_numerical())

        if len(all_scenarios_so_far) > 0:
            if(len(self.important_columns) > 0):
                for idx in self.important_columns:
                    numbers = [idx + i for i in range(self.num_features_to_consider)]

                    selected_columns_with_recovery = np.zeros((len(all_scenarios_so_far), len(numbers) + 1), dtype='int')
                    selected_columns_with_recovery[:, np.arange(len(numbers))] = np.array(all_scenarios_so_far)[:, numbers]
                    selected_columns_with_recovery[:, -1] = [self.recovery_behaviors.index(recovery_behavior) for recovery_behavior in corresponding_recoveries_for_scenarios_so_far]
                    unique_selected_columns_with_recovery = np.unique(selected_columns_with_recovery, axis=0)
                    unique_selected_columns_without_recovery = np.unique(selected_columns_with_recovery[:, :-1], axis=0)

                    # Count the amount of times this location appears in combination with a different recovery
                    # essentially determening the relevancy of this location:
                    # if the location is relevant then the recovery will always be the same and thus will negative = 0
                    # otherwise negative will be positive
                    negative = len(unique_selected_columns_with_recovery) - len(unique_selected_columns_without_recovery)

                    # only keep track of relevant locations
                    if negative <= 0:
                        should_change = False
                        self.combination_feature_weights[str(numbers)] = 1
                    else:
                        mask = self.important_columns != idx
                        self.important_columns = self.important_columns[mask]
                        self.combination_feature_weights.pop(str(numbers), None)
            else:
                should_change = True
                self.important_columns = np.arange(self.num_of_columns)
        return should_change

    def update_baf(self, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.current_best_recovery_behavior = best_recovery_behavior
        recovery_behavior_index = self.add_recovery_behavior()
        if self.compute_combination_feature_weights(recovery_behavior_index, all_scenarios_so_far,
                                                    corresponding_recoveries_for_scenarios_so_far):
            self.num_features_to_consider += 1

    def add_recovery_behavior(self):
        if self.current_best_recovery_behavior not in self.recovery_behaviors:
            self.recovery_behaviors.append(self.current_best_recovery_behavior)
        return self.recovery_behaviors.index(self.current_best_recovery_behavior)

    def most_common(self,lst):
        return max(set(lst), key=lst.count)

    def guess(self, previous_scenarios,
                                                          previous_best_recoveries):
        if self.combination_feature_weights == {}:
            return ''

        for key, value in self.combination_feature_weights.items():
            relevant_column = ast.literal_eval(key)
            break

        current_object = list(np.array(self.gen[0].scenario_to_numerical())[relevant_column])
        recovery_behavior_weights = {}
        for recovery_behavior in self.recovery_behaviors:
            recovery_behavior_weights[recovery_behavior] = 0
        for recovery_behavior in self.recovery_behaviors:
            for idx, prev_scenario in enumerate(previous_scenarios):
                if (recovery_behavior == previous_best_recoveries[idx]) and (
                        str(current_object) == str(list(np.array(prev_scenario)[relevant_column]))):
                    recovery_behavior_weights[
                        previous_best_recoveries[idx]] += 1

        max_val = max([v for k,v in recovery_behavior_weights.items()])
        max_behaviors = [k for k,v in recovery_behavior_weights.items() if v==max_val]
        if len(max_behaviors) == 1:
            return max_behaviors[0]
        else:
            return self.most_common(previous_best_recoveries)

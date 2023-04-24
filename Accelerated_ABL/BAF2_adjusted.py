import itertools
import numpy as np
import operator


class BAF2:
    gen = [0]

    def __init__(self, scenario, gen):
        self.gen[0] = gen
        self.support_weights = {}
        self.combination_feature_weights = {}
        self.subsets = []
        self.recovery_behaviors = []
        self.support_repetitions = {}
        self.current_best_recovery_behavior = "Nothing"
        self.init_phase=True
        self.num_features_to_consider = 1
        self.most_common_is_best = 0


    def recur_subset(self, s, l=None):
        if l is None:
            l = len(s)
            self.subsets = []
        if 0 < l <= self.num_features_to_consider:
            for x in itertools.combinations(s, l):
                numbers = self.arg_to_combination_numbers(x)
                if self.init_phase or (str(numbers) in self.combination_feature_weights):
                    if len(numbers) == self.num_features_to_consider:
                        self.subsets.append(list(x))
            self.recur_subset(s, l - 1)
        if l > self.num_features_to_consider:
            self.recur_subset(s, l - 1)

    def arg_to_combination_numbers(self, argument1):
        lst = []
        for arg in argument1:
            if len(arg) == 3:
                lst.append(arg[0] * 2)
                lst.append(arg[0] * 2 + 1)
            elif len(arg) == 2:
                if arg[1] in ['red', 'green', 'blue', 'yellow']:
                    lst.append(arg[0] * 2)
                else:
                    lst.append(arg[0] * 2 + 1)
        return lst

    def enumerate_scenarios(self, scenario):
        enumerated_scenarios = []
        for idx in range(len(scenario)):
                enumerated_scenarios.append([idx, scenario[idx][0], scenario[idx][1]])
        return enumerated_scenarios

    def compute_combination_feature_weights(self, best_recovery_behavior_idx, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        should_change = True
        numerical_scenario = np.array(self.gen[0].scenario_to_numerical())
        if len(all_scenarios_so_far) > 0:
            self.init_phase = False
            for idx, subset in enumerate(self.subsets):
                numbers = self.arg_to_combination_numbers(subset)
                selected_columns_with_recovery = np.zeros((len(all_scenarios_so_far), len(numbers) + 1), dtype='int')
                selected_columns_with_recovery[:, np.arange(len(numbers))] = np.array(all_scenarios_so_far)[:, numbers]
                selected_columns_with_recovery[:, -1] = [self.recovery_behaviors.index(recovery_behavior) for recovery_behavior in corresponding_recoveries_for_scenarios_so_far]
                unique_selected_columns_with_recovery = np.unique(selected_columns_with_recovery, axis=0)
                unique_selected_columns_without_recovery = np.unique(selected_columns_with_recovery[:, :-1], axis=0)
                positive = len(selected_columns_with_recovery) - len(unique_selected_columns_with_recovery)
                negative = len(unique_selected_columns_with_recovery) - len(unique_selected_columns_without_recovery)

                overal = positive + 1 + negative * (-50)

                if negative <= 0:
                    should_change = False
                    self.combination_feature_weights[str(numbers)] = overal
                else:
                    self.combination_feature_weights.pop(str(numbers), None)
        else:
            should_change = False
        return should_change

    def update_baf(self, scenario, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.current_best_recovery_behavior = best_recovery_behavior
        enumerated_scenarios = self.enumerate_scenarios(scenario)
        self.recur_subset(enumerated_scenarios)
        recovery_behavior_index = self.add_recovery_behavior()
        if self.compute_combination_feature_weights(recovery_behavior_index, all_scenarios_so_far,
                                                    corresponding_recoveries_for_scenarios_so_far):
            self.num_features_to_consider += 1
            self.init_phase = True

    def add_recovery_behavior(self):
        if self.current_best_recovery_behavior not in self.recovery_behaviors:
            self.recovery_behaviors.append(self.current_best_recovery_behavior)
        return self.recovery_behaviors.index(self.current_best_recovery_behavior)

    def most_common(self,lst):
        return max(set(lst), key=lst.count)

    def compute_sum_of_weights_for_each_recovery_behavior(self, scenario, previous_scenarios,
                                                          previous_best_recoveries):
        if self.combination_feature_weights == {}:
            print("combination_feature_weights is empty, returning nothing")
            return ''
        max_weighted_combinations_key = ""
        max_weighted_combinations_value = -10000
        for key, value in self.combination_feature_weights.items():
            if value > max_weighted_combinations_value:
                max_weighted_combinations_value = value
                max_weighted_combinations_key = key
        max_indices_list = max_weighted_combinations_key.split('[')[1].split(']')[0].split(',')
        max_indices_list = list(map(int, max_indices_list))
        current_scenarios_columns = list(np.array(self.gen[0].scenario_to_numerical())[max_indices_list])
        recovery_behavior_weights = {}
        for recovery_behavior in self.recovery_behaviors:
            recovery_behavior_weights[recovery_behavior] = 0
        for recovery_behavior in self.recovery_behaviors:
            for idx, prev_scenario in enumerate(previous_scenarios):
                if (recovery_behavior == previous_best_recoveries[idx]) and (
                        str(current_scenarios_columns) == str(list(np.array(prev_scenario)[max_indices_list]))):
                    recovery_behavior_weights[
                        previous_best_recoveries[idx]] += 1
        
        if recovery_behavior_weights != {}:
            max_val = max([v for k,v in recovery_behavior_weights.items()])
            max_behaviors = [k for k,v in recovery_behavior_weights.items() if v==max_val]
            if len(max_behaviors) == 1:
                print("confidently returning", max_behaviors[0])
                return max_behaviors[0]
            else:
                print("returning most_common", self.most_common(previous_best_recoveries))
                return self.most_common(previous_best_recoveries)
        else:
            print('returning nothing')
            return ''

    def generate_second_guess(self, scenario, previous_scenarios, previous_best_recoveries):
        # Extract features
        enumerated_scenarios = self.enumerate_scenarios(scenario)
        self.recur_subset(enumerated_scenarios)
        
        return self.compute_sum_of_weights_for_each_recovery_behavior(enumerated_scenarios, previous_scenarios,
                                                                      previous_best_recoveries)
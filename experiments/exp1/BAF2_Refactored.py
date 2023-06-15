import numpy as np
import itertools

class BAF2:
    def __init__(self, scenario):
        self.possible_location_combinations = []
        self.recovery_behaviors = []
        self.num_features_to_consider = 1
        self.weights = {}
        self.num_of_locations = len(scenario) * 2
        important_locations = np.arange(self.num_of_locations)
        combinations = list(itertools.combinations(important_locations, self.num_features_to_consider))
        self.combinations_as_lists = [list(comb) for comb in combinations] 

    def determine_relevant_locations(self, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        if len(all_scenarios_so_far) > 0:
            if(len(self.combinations_as_lists) == 0):
                self.num_features_to_consider += 1
                important_locations = np.arange(self.num_of_locations)
                combinations = list(itertools.combinations(important_locations, self.num_features_to_consider))
                self.combinations_as_lists = [list(comb) for comb in combinations] 

            copy_of_combinations_as_list =  self.combinations_as_lists[:]
            for numbers in copy_of_combinations_as_list:
                selected_locations_with_recovery = np.zeros((len(all_scenarios_so_far), len(numbers) + 1), dtype='int')
                selected_locations_with_recovery[:, np.arange(len(numbers))] = np.array(all_scenarios_so_far)[:, numbers]
                selected_locations_with_recovery[:, -1] = [self.recovery_behaviors.index(recovery_behavior) for recovery_behavior in corresponding_recoveries_for_scenarios_so_far]
                unique_selected_locations_with_recovery = np.unique(selected_locations_with_recovery, axis=0)
                unique_selected_locations_without_recovery = np.unique(selected_locations_with_recovery[:, :-1], axis=0)

                # Count the amount of times the object in this location appears in combination with a different recovery
                # essentially determening the relevancy of this location:
                # if the location is relevant then the recovery will always be the same for the same object and thus will negative = 0
                # otherwise negative will be positive
                negative = len(unique_selected_locations_with_recovery) - len(unique_selected_locations_without_recovery)

                # only keep track of relevant locations
                if negative <= 0:
                    if numbers not in self.possible_location_combinations:
                        self.possible_location_combinations.append(numbers)
                        self.weights[str(numbers)] = len(selected_locations_with_recovery) - len(unique_selected_locations_with_recovery)
                else:
                    self.combinations_as_lists.remove(numbers)
                    if numbers in self.possible_location_combinations:
                        self.possible_location_combinations.remove(numbers)
        return

    def update_baf(self, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.add_recovery_behavior(best_recovery_behavior)
        self.determine_relevant_locations(all_scenarios_so_far, corresponding_recoveries_for_scenarios_so_far)

    def add_recovery_behavior(self, brb):
        if brb not in self.recovery_behaviors:
            self.recovery_behaviors.append(brb)

    def most_common(self,lst):
        return max(set(lst), key=lst.count)

    def guess(self, current_scenario, previous_scenarios, previous_best_recoveries):
        if not self.possible_location_combinations:
            # list is empty
            return ''

        max_weight = -1
        for instance in self.possible_location_combinations:
            if self.weights[str(instance)] > max_weight:
                max_weight = self.weights[str(instance)]
                relevant_locations = instance
            
        # Acquire the current objects we are looking at
        # (make it a list for easier comparrison)
        current_objects = list(np.array(current_scenario)[relevant_locations])

        recovery_behavior_weights = {}
        for recovery_behavior in self.recovery_behaviors:
            recovery_behavior_weights[recovery_behavior] = 0
        for recovery_behavior in self.recovery_behaviors:
            for idx, prev_scenario in enumerate(previous_scenarios):
                if (recovery_behavior == previous_best_recoveries[idx]) and (
                        current_objects == list(np.array(prev_scenario)[relevant_locations])):
                    recovery_behavior_weights[recovery_behavior] += 1

        max_val = max([v for k,v in recovery_behavior_weights.items()])
        max_behaviors = [k for k,v in recovery_behavior_weights.items() if v==max_val]

        if len(max_behaviors) == 1:
            return max_behaviors[0]
        else:
            return self.most_common(previous_best_recoveries)
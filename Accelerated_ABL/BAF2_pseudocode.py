import numpy as np

class BAF2:
    def __init__(self, scenario):
        self.possible_location_combinations = []
        self.recovery_behaviors = []
        self.num_features_to_consider = 1
        self.num_of_locations = len(scenario)
        self.important_locations = np.arange(self.num_of_locations)

    def determine_relevant_locations(self, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        should_change = False
        if len(all_scenarios_so_far) > 0:
            if(len(self.important_locations) > 0):
                for idx in self.important_locations:

                    numbers = [idx + i for i in range(self.num_features_to_consider)]
                    selected_locations_with_recovery = np.zeros((len(all_scenarios_so_far), len(numbers) + 1), dtype='int')
                    selected_locations_with_recovery[:, np.arange(len(numbers))] = np.array(all_scenarios_so_far)[:, numbers]
                    selected_locations_with_recovery[:, -1] = [self.recovery_behaviors.index(recovery_behavior) for recovery_behavior in corresponding_recoveries_for_scenarios_so_far]
                    unique_selected_locations_with_recovery = np.unique(selected_locations_with_recovery, axis=0)
                    unique_selected_locations_without_recovery = np.unique(selected_locations_with_recovery[:, :-1], axis=0)

                    # Count the amount of times this location appears in combination with a different recovery
                    # essentially determening the relevancy of this location:
                    # if the location is relevant then the recovery will always be the same and thus will negative = 0
                    # otherwise negative will be positive
                    negative = len(unique_selected_locations_with_recovery) - len(unique_selected_locations_without_recovery)

                    # only keep track of relevant locations
                    if negative <= 0:
                        should_change = False
                        if numbers not in self.possible_location_combinations:
                            self.possible_location_combinations.append(numbers)
                    else:
                        mask = self.important_locations != idx
                        self.important_locations = self.important_locations[mask]
                        if numbers in self.possible_location_combinations:
                            self.possible_location_combinations.remove(numbers)
            else:
                should_change = True
                self.important_locations = np.arange(self.num_of_locations)
        return should_change

    def update_baf(self, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.add_recovery_behavior(best_recovery_behavior)
        if self.determine_relevant_locations(all_scenarios_so_far, corresponding_recoveries_for_scenarios_so_far):
            self.num_features_to_consider += 1

    def add_recovery_behavior(self, brb):
        if brb not in self.recovery_behaviors:
            self.recovery_behaviors.append(brb)

    def most_common(self,lst):
        return max(set(lst), key=lst.count)

    def guess(self, current_scenario, previous_scenarios, previous_best_recoveries):
        if not self.possible_location_combinations:
            # list is empty
            return ''

        relevant_locations = self.possible_location_combinations[0]

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
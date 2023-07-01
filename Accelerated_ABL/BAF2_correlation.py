import numpy as np
import itertools
from collections import Counter


class BAF2:
    def __init__(self, scenario):
        self.possible_location_combinations = []
        self.recovery_behaviors = []
        self.num_features_to_consider = 1
        self.weights = {}
        self.num_of_locations = len(scenario) * 2
        self.important_locations = []

    def determine_relevant_locations(self, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        self.important_locations = []
        data_array = np.array(all_scenarios_so_far)
        correlations = np.corrcoef(data_array, corresponding_recoveries_for_scenarios_so_far)
        column_correlations = correlations[:-1, -1]

        for i in range(data_array.shape[1]):
            


        for i, correlation in enumerate(column_correlations):
            if correlation == 1:
                self.important_locations.append(i)
            print(f"Correlation between column {i+1} and second list: {correlation}")
        

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
        if not self.important_locations:
            # list is empty
            return ''
        data_array = np.array(previous_scenarios)
        recoveries = []
        for column in self.important_locations:
        # Find the indices of rows where the item from 'list_items' is present in the current column
            matching_rows = np.where(data_array[:, column] == current_scenario[column])[0]
            for row in matching_rows:
                recoveries.append(previous_best_recoveries[row])
        
        string_counts = Counter(recoveries)
        most_common_string = string_counts.most_common(1)[0][0]
           
        return most_common_string
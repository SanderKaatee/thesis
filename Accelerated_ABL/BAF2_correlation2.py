import numpy as np
import statistics
from collections import Counter

class BAF2:
    def __init__(self, scenario):
        self.important_locations = []

    def determine_relevant_locations(self, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        self.important_locations = []
        
        correlating_columns = {}

        # Transpose the 2D list to make columns easier to handle
        transposed_scenarios = list(map(list, zip(*all_scenarios_so_far)))

        # Check each column
        for i, column in enumerate(transposed_scenarios):
            # Create a dictionary to map each scenario to a recovery
            scenario_to_recovery = {}
            correlating_columns[i] = 0
            # If the mappings in the dictionary recreate the original lists exactly, then the column is a correlating column
            # Thus we count how many rows are the same as the original list
            for scenario, recovery in zip(column, corresponding_recoveries_for_scenarios_so_far):
                if scenario in scenario_to_recovery:
                    if scenario_to_recovery[scenario] == recovery:
                        correlating_columns[i] += 1
                else:
                    scenario_to_recovery[scenario] = recovery

            # Normalize to percentages
            correlating_columns[i] = correlating_columns[i] / len(column)
        
        if correlating_columns:
            mode_value = statistics.mode(correlating_columns.values())        
            keys_above_mode = [key for key, value in correlating_columns.items() if value > mode_value]
            self.important_locations = keys_above_mode

        return

    # such that it fits with previous experiments
    def update_baf(self, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.determine_relevant_locations(all_scenarios_so_far, corresponding_recoveries_for_scenarios_so_far)

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

        # If no rows matched, return the most common recovery over all previously seen recoveries
        if not string_counts:
            string_counts = Counter(previous_best_recoveries)
        
        most_common_string = string_counts.most_common(1)[0][0]

        return most_common_string
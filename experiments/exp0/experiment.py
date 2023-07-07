"""
Created on Thursday Oct 13 2020
@author: Hamed Ayoobi
َAll rights reserved 2020
"""

"""
Adjustments by Sander Kaatee:
- scenario_type as argument
- measure run times per algorithm
- save experiment data to .csv
- changed the amount of plots saved
"""


import scenarios
import BAF2
import BAF
from sklearn import tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
import sys
import csv
import os
import tempfile
import shutil

from timeit import default_timer as timer

if __name__ == "__main__":
    number_of_attempts = 200
    number_of_iterations = 1
    all_TPs = np.zeros((number_of_iterations,number_of_attempts))
    all_TPs_Orig = np.zeros((number_of_iterations, number_of_attempts))
    all_DT_TPs = np.zeros((number_of_iterations, number_of_attempts))

    if len(sys.argv) > 1:
        scenario_type = sys.argv[1]
        print("scenario_type:", scenario_type)
    else:
        scenario_type = "first" #options are "first" and "second"

    ABL_correct = []
    AABL_correct = []
    DT_correct = []

    runtimes = {'ABL': 0, 'AABL': 0}



    start_time = time.process_time()
    times = []
    for itr in range(number_of_iterations):
        print(f"\n\n {itr} / {number_of_iterations - 1} \n\n")
        gen = scenarios.ScenarioGenerator(scenario_type)
        baf = BAF2.BAF2(gen.scenario, gen)
        # baf2 = BAF.BAF(gen.scenario)
        saved_scenarios_in_memory_for_other_approaches = []
        saved_best_recovery_behaviors_in_memory_for_other_approaches = []
        TP = 0
        # TP_Orig = 0
        DT_TP = 0
        feature_indices = []
        # time.sleep(10)
        start = timer()
        for attempt in range(number_of_attempts):
            start = timer()
            gen.generate_scenario()
            guess = baf.generate_second_guess(gen.scenario, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, show_rule=True)
            baf.update_baf(gen.scenario, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)
            if gen.best_recovery_behavior == guess:
                TP += 1
            all_TPs[itr, attempt] = TP
            runtimes['AABL'] += timer()-start

            # start = timer()
            # # guess_orig = baf2.generate_second_guess(gen.scenario, show_rule=True)
            # # baf2.update_baf(gen.scenario, gen.best_recovery_behavior)
            # if random.randint(0,100) < 90 or attempt < 3:
            #     if gen.best_recovery_behavior == guess_orig:
            #         TP_Orig += 1
            # elif gen.best_recovery_behavior == [value for (key,value) in gen.recovery_behaviors.items()][random.randint(0,3)]:
            #     TP_Orig += 1
            # all_TPs_Orig[itr, attempt] = TP_Orig
            # runtimes['ABL'] += timer()-start

            #Decision tree with sklearn
            if saved_scenarios_in_memory_for_other_approaches:
                clf = tree.DecisionTreeClassifier()
                clf = clf.fit(saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)
                dt_guess = gen.numerical_to_recovery_behavior(clf.predict([gen.scenario_to_numerical()])[0])
                if dt_guess == gen.best_recovery_behavior:
                    DT_TP += 1
                all_DT_TPs[itr, attempt] = DT_TP
                # tree.plot_tree(clf)
                # plt.show()



            saved_scenarios_in_memory_for_other_approaches.append(gen.scenario_to_numerical())
            saved_best_recovery_behaviors_in_memory_for_other_approaches.append(gen.recovery_behavior_to_numerical())
            # if attempt == 0:
            #     time.sleep(10)
            # print(f"time: {timer()-start} s")
            print(f"{attempt}:Our: {TP},")

        AABL_correct.append(TP)
        # ABL_correct.append(TP_Orig)
        DT_correct.append(DT_TP)




        one_iteration_time = timer() - start
        times.append(one_iteration_time)
        print("average_per_iteration_time: ", np.mean(times))
        # time.sleep(100)
        print(f"Our model true positives: {TP}")
        # print(f"Our original model true positives: {TP_Orig}")
        print(f"Decision Tree's true positives: {DT_TP}")
        print(f"Overal: {np.mean(all_TPs[:itr+1],axis=0)}")
        # print(f"Original Overal accuracy: {np.mean(all_TPs_Orig[:itr+1],axis=0)/(np.array(range(number_of_attempts)) + 1)}")
        # print(f"Original Overal: {np.mean(all_TPs_Orig[:itr+1],axis=0)}")
        print(f"Overal accuracy: {np.mean(all_TPs[:itr+1],axis=0)/(np.array(range(number_of_attempts)) + 1)}")
        print(f"Overal DT: {np.mean(all_DT_TPs,axis=0)}")
        fig, ax = plt.subplots(nrows=1, ncols=1)
        print(f"Overal DT accuracy: {np.mean(all_DT_TPs[:itr+1],axis=0)/(np.array(range(number_of_attempts)) + 1)}")
        ax.plot(range(number_of_attempts), np.mean(all_TPs[:itr+1], axis=0)/(np.array(range(number_of_attempts)) + 1), 'r-', label="AABL")
        # ax.plot(range(number_of_attempts),
                # np.mean(all_TPs_Orig[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), '--', label="Original ABL")
        ax.set_xlabel("Number of Attempts")
        ax.set_ylabel("Accuracy")
        # ax.plot(range(number_of_attempts), np.mean(all_DT_TPs[:itr+1], axis=0)/(np.array(range(number_of_attempts)) + 1), 'r-', label="Decision Tree")
        ax.legend()
        if itr == number_of_iterations - 1: #only the final plot will be shown (all the plots has been saved)
            fig.savefig(f"plots/exp0_fig_{scenario_type}.png", bbox_inches='tight')
        plt.close(fig)

    
    data = pd.DataFrame({
        'iteration': range(1, number_of_iterations + 1),
        'AABL_correct': AABL_correct,
    })
    csv_filename = './data/runtime.csv'
    if not os.path.isfile(csv_filename):
        header = ['scenario', 'AABL']
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

    # Read existing data from the CSV file
    with open(csv_filename, 'r') as csvfile, tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_file)

        # Iterate over the rows
        write_new_row = True
        for row in reader:
            # Check if the condition matches in the first column
            if row[0] != scenario_type:
                writer.writerow(row)
            else:
                write_new_row = False
                writer.writerow([scenario_type, runtimes['AABL']])
        if write_new_row:
            writer.writerow([scenario_type, runtimes['AABL']])

    shutil.move(temp_file.name, csv_filename)


    print(f"Mean Process Time = {np.mean(times)}")
    end_time = time.process_time()
    print(f"Total Process Time = {end_time - start_time}")
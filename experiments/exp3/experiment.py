"""
Based on:
Created on Thursday Oct 13 2020
@author: Hamed Ayoobi
َAll rights reserved 2020
"""

import scenario_2b as scenarios
import BAF2 as BAF2
from BAF2_Refactored import RABL
from string_counter import StringCounter
import pseudocode as myABL


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


def main():
    number_of_attempts = 1000
    number_of_iterations = 5
    all_TPs_AABL = np.zeros((number_of_iterations,number_of_attempts))
    all_TPs_RABL = np.zeros((number_of_iterations, number_of_attempts))
    all_TPs_pseudo = np.zeros((number_of_iterations, number_of_attempts))
    all_TPs_mostcommon = np.zeros((number_of_iterations, number_of_attempts))
    
    if len(sys.argv) > 1:
        scenario_type = sys.argv[1]
        print("scenario_type:", scenario_type)
    else:
        scenario_type = "first" #options are "first" and "second"

    pseudocode_correct = []
    AABL_correct = []
    RABL_correct = []
    mostcommon_correct = []

    runtimes = {'AABL': 0, 'pseudocode': 0, 'RABL': 0}


    start_time = time.process_time()
    for itr in range(number_of_iterations):
        gen = scenarios.ScenarioGenerator(scenario_type)
        baf = BAF2.BAF2(gen.scenario, gen)
        pseudo = myABL.BAFUnit()
        rabl = RABL(gen.scenario)
        mostcommon = StringCounter()

        saved_scenarios_in_memory_for_other_approaches = []
        saved_best_recovery_behaviors_in_memory_for_other_approaches = []
        saved_best_recovery_behaviors_in_memory = []

        all_scenarios = []
        all_recoveries = []
        TP_AABL = 0
        TP_RABL = 0
        TP_pseudo = 0
        TP_mostcommon = 0

        for attempt in range(number_of_attempts):
            gen.generate_scenario()


            start = timer()
            guess = baf.generate_second_guess(gen.scenario, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, show_rule=True)
            baf.update_baf(gen.scenario, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)
            if gen.best_recovery_behavior == guess:
                TP_AABL += 1
            all_TPs_AABL[itr, attempt] = TP_AABL
            runtimes['AABL'] += timer()-start


            start = timer()
            guess = pseudo.AABL(gen.scenario, gen.best_recovery_behavior)
            if guess == gen.best_recovery_behavior:
                TP_pseudo += 1
            all_TPs_pseudo[itr, attempt] = TP_pseudo
            runtimes['pseudocode'] += timer()-start

            start = timer()
            all_scenarios.append(gen.scenario_to_numerical())
            all_recoveries.append(gen.best_recovery_behavior)
            guess = rabl.guess(gen.scenario_to_numerical(), saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            rabl.update_baf(gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            if gen.best_recovery_behavior == guess:
                TP_RABL += 1
            all_TPs_RABL[itr, attempt] = TP_RABL
            runtimes['RABL'] += timer()-start

            guess = mostcommon.guess()
            if gen.best_recovery_behavior == guess:
                TP_mostcommon += 1
            all_TPs_mostcommon[itr,attempt] = TP_mostcommon
            mostcommon.update(gen.best_recovery_behavior)



            saved_scenarios_in_memory_for_other_approaches.append(gen.scenario_to_numerical())
            saved_best_recovery_behaviors_in_memory_for_other_approaches.append(gen.recovery_behavior_to_numerical())

            saved_best_recovery_behaviors_in_memory.append(gen.best_recovery_behavior)
 
            print(f"{attempt}:AABL: {TP_AABL}, RABL: {TP_RABL}, pseudo: {TP_pseudo}, mostcommon: {TP_mostcommon}")
            print("best recovery was", gen.best_recovery_behavior)
            # input("Press any key...")
            pseudocode_correct.append(TP_pseudo)
            AABL_correct.append(TP_AABL)
            RABL_correct.append(TP_RABL)
            mostcommon_correct.append(TP_mostcommon)



        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(range(number_of_attempts), np.mean(all_TPs_AABL[:itr+1], axis=0)/(np.array(range(number_of_attempts)) + 1), 'r-', label="AABL")
        ax.plot(range(number_of_attempts), np.mean(all_TPs_RABL[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), 'b:', label="RABL")
        ax.plot(range(number_of_attempts), np.mean(all_TPs_pseudo[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), '--', label="pseudocode")
        ax.plot(range(number_of_attempts), np.mean(all_TPs_mostcommon[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), '-.', label="mostcommon")
        ax.set_xlabel("Number of Attempts")
        ax.set_ylabel("Accuracy")
        ax.legend()
        if itr == number_of_iterations - 1: #only the final plot will be shown (all the plots has been saved)
            fig.savefig(f"plots/exp1_fig_{scenario_type}.png", bbox_inches='tight')
        plt.close(fig)
    end_time = time.process_time()
    print(f"Total Process Time = {end_time - start_time}")
    

    data = pd.DataFrame({
        'AABL_correct': AABL_correct,
        'pseudocode_correct': pseudocode_correct,
    })
    data.to_csv('data/result_' + scenario_type + '.csv', index=False)

    csv_filename = './data/runtime.csv'
    if not os.path.isfile(csv_filename):
        header = ['scenario', 'AABL', 'RABL', 'pseudocode']
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
                writer.writerow([scenario_type, runtimes['AABL'], runtimes['RABL'], runtimes['pseudocode']])
        if write_new_row:
            writer.writerow([scenario_type, runtimes['AABL'], runtimes['RABL'], runtimes['pseudocode']])

    shutil.move(temp_file.name, csv_filename)


if __name__ == "__main__":
    main()
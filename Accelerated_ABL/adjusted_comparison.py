"""
Created on Thursday Oct 13 2020
@author: Hamed Ayoobi
َAll rights reserved 2020
"""

import sys
import scenarios_original as scenarios
import BAF2_original as BAF2
import BAF2_correlation as myABL
import BAF2_correlation2 as myABL2
import tabular
from sklearn import tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from timeit import default_timer as timer


def main():
    number_of_attempts = 200
    number_of_iterations = 10
    all_TPs = np.zeros((number_of_iterations,number_of_attempts))
    all_TPs_Orig = np.zeros((number_of_iterations, number_of_attempts))
    all_TPs_my = np.zeros((number_of_iterations, number_of_attempts))
    all_TPs_my2 = np.zeros((number_of_iterations, number_of_attempts))
    all_TPs_tabular = np.zeros((number_of_iterations, number_of_attempts))
    scenario_type = "third" #options are "first" and "second"

    refactored_correct = []
    refactored_incorrect = []
    AABL_correct = []
    AABL_incorrect = []
    My_time = 0
    My_time2 = 0
    AABL_time = 0




    start_time = time.process_time()
    for itr in range(number_of_iterations):
        gen = scenarios.ScenarioGenerator(scenario_type)
        baf = BAF2.BAF2(gen.scenario, gen)
        myBAF = myABL.BAF2(gen.scenario)
        myBAF2 = myABL2.BAF2(gen.scenario)
        locations = list(range(0, gen.number_of_locations))
        colors = list(gen.colors.values())
        colors.append("Noc")
        concepts = list(gen.concepts.values())
        concepts.append("Noc")
        actions = list(gen.recovery_behaviors.values())
        Qlearn = tabular.TabularQLearning(locations, colors, concepts, actions)

        saved_scenarios_in_memory_for_other_approaches = []
        saved_best_recovery_behaviors_in_memory_for_other_approaches = []
        saved_best_recovery_behaviors_in_memory = []

        all_scenarios = []
        all_recoveries = []
        TP = 0
        TP_Orig = 0
        TP_my = 0
        TP_my2 = 0
        TP_tabular = 0
        DT_TP = 0

        Orig_time = 0
        Tabular_time = 0
        feature_indices = []
        for attempt in range(number_of_attempts):
            gen.generate_scenario()


            # start = timer()
            # guess = baf.generate_second_guess(gen.scenario, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, show_rule=True)
            # baf.update_baf(gen.scenario, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)
            # if gen.best_recovery_behavior == guess:
            #     TP += 1
            # all_TPs[itr, attempt] = TP
            # # print(f"AABL: {timer()-start} s")
            # AABL_time += timer()-start

            # start = timer()
            # guess_orig = baf2.generate_second_guess(gen.scenario, show_rule=True)
            # baf2.update_baf(gen.scenario, gen.best_recovery_behavior)
            # if random.randint(0,100) < 90 or attempt < 3:
            #     if gen.best_recovery_behavior == guess_orig:
            #         TP_Orig += 1
            # elif gen.best_recovery_behavior == [value for (key,value) in gen.recovery_behaviors.items()][random.randint(0,3)]:
            #     TP_Orig += 1
            # all_TPs_Orig[itr, attempt] = TP_Orig
            # print(f"ORIGINAL: {timer()-start} s")
            # Orig_time += timer()-start



            start = timer()
            all_scenarios.append(gen.scenario_to_numerical())
            all_recoveries.append(gen.best_recovery_behavior)
            guess = myBAF.guess(gen.scenario_to_numerical(), saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            myBAF.update_baf(gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            if gen.best_recovery_behavior == guess:
                TP_my += 1
            all_TPs_my[itr, attempt] = TP_my
            My_time += timer()-start

            start = timer()
            guess = myBAF2.guess(gen.scenario_to_numerical(), saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            myBAF2.update_baf(gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory)
            if gen.best_recovery_behavior == guess:
                TP_my2 += 1
            all_TPs_my2[itr, attempt] = TP_my2
            My_time2 += timer()-start



            saved_scenarios_in_memory_for_other_approaches.append(gen.scenario_to_numerical())
            saved_best_recovery_behaviors_in_memory_for_other_approaches.append(gen.recovery_behavior_to_numerical())

            saved_best_recovery_behaviors_in_memory.append(gen.best_recovery_behavior)
 
            print(f"{attempt}:AABL: {TP}, Adjusted: {TP_my}, extra: {TP_my2}")
            print("best recovery was", gen.best_recovery_behavior)
            # input("Press any key...")
            refactored_correct.append(TP_my)
            refactored_incorrect.append(200-TP_my)
            AABL_correct.append(TP)
            AABL_incorrect.append(200-TP)



        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(range(number_of_attempts), np.mean(all_TPs[:itr+1], axis=0)/(np.array(range(number_of_attempts)) + 1), 'r-', label="AABL")
        ax.plot(range(number_of_attempts), np.mean(all_TPs_my[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), ':', label="Refactored1")
        ax.plot(range(number_of_attempts), np.mean(all_TPs_my2[:itr + 1], axis=0) / (np.array(range(number_of_attempts)) + 1), '.-', label="Refactored2")
        ax.set_xlabel("Number of Attempts")
        ax.set_ylabel("Accuracy")
        ax.legend()
        fig.savefig(f"plots/fig_{itr}.png", bbox_inches='tight')
        if itr != number_of_iterations - 1: #only the final plot will be shown (all the plots has been saved)
            plt.close(fig)
    end_time = time.process_time()
    print(f"Total Process Time = {end_time - start_time}")
    print("AABL time", AABL_time)
    print("Refactored time", My_time)
    print("AABL memory", sys.getsizeof(baf))
    print("Refactored memory", sys.getsizeof(myBAF))
    

    data = pd.DataFrame({
        'AABL_correct': AABL_correct,
        'AABL_incorrect': AABL_incorrect,
        'refactored_correct': refactored_correct,
        'refactored_incorrect': refactored_incorrect
    })
    data.to_csv('refactored_result_' + scenario_type + '.csv', index=False)
    plt.show()

if __name__ == "__main__":
    main()
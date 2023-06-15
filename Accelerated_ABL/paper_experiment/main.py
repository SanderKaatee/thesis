import BAF2 as BAF2
import scenario_paper as scenarios


gen = scenarios.ScenarioGenerator()
baf = BAF2.BAF2(gen.scenario, gen)

saved_scenarios_in_memory_for_other_approaches = []
saved_best_recovery_behaviors_in_memory_for_other_approaches = []




for i in range(13):
    gen.generate_scenario()
    print("scenario:", gen.scenario)
    guess = baf.generate_second_guess(gen.scenario, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, show_rule=True)
    print("guess:", guess)
    baf.update_baf(gen.scenario, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)

    saved_scenarios_in_memory_for_other_approaches.append(gen.scenario_to_numerical())
    saved_best_recovery_behaviors_in_memory_for_other_approaches.append(gen.recovery_behavior_to_numerical())
    input("\n")





#!/bin/bash

# Loop through each subfolder
for subfolder in */; do
  # Change directory to the subfolder
  cd "$subfolder" || continue
  
  # Check if the run_experiment.sh file exists in the subfolder
  if [[ -f "run_experiment.sh" ]]; then
    # Execute the run_experiment.sh script in the background
    bash "run_experiment.sh" &
  fi
  
  # Change back to the main folder
  cd ".." || exit
done

# Wait for all background processes to finish
wait

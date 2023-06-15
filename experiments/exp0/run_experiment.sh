#!/bin/bash

# Define the arguments to be passed
arguments=("first" "second" "third")

# Loop through the arguments
for argument in "${arguments[@]}"
do
    # Run the Python script with the current argument
    python experiment.py $argument
done
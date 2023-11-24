#!/bin/bash

# Run run_hard_GCP with different models
python run/run_hard_GCP.py gpt-4-1106-preview &
python run/run_hard_GCP.py gpt-3.5-turbo &
python run/run_hard_GCP.py claude-2 &
python run/run_hard_GCP.py claude-instant-1.2 &

# Run run_hard_MSP with different models
python run/run_hard_MSP.py gpt-4-1106-preview &
python run/run_hard_MSP.py gpt-3.5-turbo &
python run/run_hard_MSP.py claude-2 &
python run/run_hard_MSP.py claude-instant-1.2 &

# Run run_hard_TSP with different models
python run/run_hard_TSP.py gpt-4-1106-preview &
python run/run_hard_TSP.py gpt-3.5-turbo &
python run/run_hard_TSP.py claude-2 &
python run/run_hard_TSP.py claude-instant-1.2 &

# Wait for all background jobs to finish
wait

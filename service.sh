#!/bin/bash

# Define your directory paths
left_directory="/home/pi/water_heaters_testings/dcs/build/debug"
right_directory="/home/pi/client"

# Create a new tmux session named "service"
tmux new-session -d -s service

# Split the session horizontally
tmux split-window -h -t service

# Execute "./sample2" in the left window
tmux send-keys -t service:0.0 "cd $left_directory" C-m
tmux send-keys -t service:0.0 "./sample2" C-m

# Execute "watch" command in the right window to run "check_service.py" every minute
tmux send-keys -t service:0.1 "cd $right_directory" C-m
tmux send-keys -t service:0.1 "watch -n 60 python3 check_service.py" C-m

# Attach to the tmux session
tmux attach-session -t service

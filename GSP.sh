#!/bin/bash

# Start a new TMUX session named "GSP"
tmux new-session -d -s GSP

# Split the window horizontally
tmux split-window -h

# Send commands to each pane
tmux send-keys -t GSP:0.0 'python3 GSP.py' C-m
tmux send-keys -t GSP:0.1 'python3 derms_1.py' C-m

# Attach to the new session
tmux attach-session -t GSP
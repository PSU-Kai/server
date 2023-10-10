#!/bin/bash

# Name of the first tmux session
SESSION_NAME1="server"

# Directory where the first script is located
SCRIPT_DIR1="/home/pi/water_heaters_testings/dcs/build/debug"

# Command to execute the first Python script
PYTHON_SCRIPT1="python3 dcm_log_data.py"

# Name of the second tmux session
SESSION_NAME2="DERMS"

# Directory where the second script is located
SCRIPT_DIR2="/home/pi/client"

# Command to execute the second Python script
PYTHON_SCRIPT2="python3 client_new.py"

# Function to create a new tmux session
create_tmux_session() {
    local session_name="$1"
    local script_dir="$2"
    local python_script="$3"
    
    # Check if the session exists
    tmux has-session -t "$session_name" 2>/dev/null

    if [ $? != 0 ]; then
        # If the session doesn't exist, create it
        tmux new-session -d -s "$session_name" -c "$script_dir"
    fi
    
    # Send the command to execute the Python script to the session
    tmux send-keys -t "$session_name" "cd $script_dir && $python_script" C-m
    
    # Attach to the tmux session
    tmux attach -t "$session_name"
}

# Create the first tmux session
create_tmux_session "$SESSION_NAME1" "$SCRIPT_DIR1" "$PYTHON_SCRIPT1"

# Create the second tmux session
create_tmux_session "$SESSION_NAME2" "$SCRIPT_DIR2" "$PYTHON_SCRIPT2"

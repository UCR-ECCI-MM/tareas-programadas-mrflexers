#!/bin/bash

# Set the path to the Streamlit app file
APP_PATH="./build/lib/health_topic_index/app.py"

# Construct the command to run Streamlit
COMMAND="streamlit run $APP_PATH ${@:1}"

# Launch Streamlit
echo "Launching the application"
$COMMAND

# Handle termination
trap "echo 'Application stopped by user'; exit" SIGINT

# Handle errors
if [ $? -ne 0 ]; then
    echo "An error occurred while launching"
fi
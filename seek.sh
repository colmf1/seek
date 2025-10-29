#!/bin/bash

# Get question from user via zenity
question=$(zenity --entry \
    --title="Enter your Question" \
    --text="What do you want to ask the AI?" \
    --width=800 \
    --height=200)

if [ -z "$question" ]; then
    zenity --error --text="No question provided. Exiting."
    exit 1
fi

output=$(python3 src/seek/main.py -q "$question")

nvim "$output"



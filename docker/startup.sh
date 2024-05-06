#!/bin/bash
# Check if the project directory is empty
if [ -z "$(ls -A /workspace)" ]; then
   # No project data present, clone a new one
   if [ -n "$GITHUB_REPO" ]; then
       git clone https://github.com/$GITHUB_REPO /workspace
   fi
fi

# Now start code-server
code-server --auth none --bind-addr 0.0.0.0:8080 /workspace

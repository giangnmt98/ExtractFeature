#!/bin/bash

# Constants
DEFAULT_PACKAGE_NAME=""
DEFAULT_CONFIG_PATH=""

# Default values
package_name="$DEFAULT_PACKAGE_NAME"
config_path="$DEFAULT_CONFIG_PATH"

# Function to parse arguments
parse_arguments() {
   while [[ "$#" -gt 0 ]]; do
       case $1 in
           --package_name)
               package_name="$2"
               shift 2
               ;;
           --config_path)
               config_path="$2"
               shift 2
               ;;
           *)
               echo "Unknown parameter passed: $1"
               exit 1
               ;;
       esac
   done
}

# Invoke argument parsing
parse_arguments "$@"


 if [ -z "$package_name" ]; then
     echo "Error: --package_name parameter is required."
     exit 1
 fi

 # Export package name
 python3 -m venv "${package_name}_env" && \
 source "${package_name}_env/bin/activate" && \
 python3 -m pip install --upgrade pip setuptools wheel && \
 python3 -m pip install -e . && \
if [ -z "$config_path" ]; then \
    echo "Running the package with a default config path." && \
    python3 "${package_name}/main.py"; \
else \
    python3 "${package_name}/main.py" --config_path "${config_path}"; \
fi
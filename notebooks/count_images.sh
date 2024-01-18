#!/bin/bash

GCS_PATH="gs://kds-435748dc60032c71c8c8d636b553f125b1f40cdc3e86846628773d16"


function process_directory {
  local dir_name="$1"
  local image_count=$(gsutil ls "${GCS_PATH}/${dir_name}/images" | wc -l)
  local label_count=$(gsutil ls "${GCS_PATH}/${dir_name}/labels" | wc -l)
  
  echo "${dir_name} images number ${image_count}, labels number ${label_count}"
}

if [ $# -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

directory="$1"

# Iterate through directories in gs://kds-435748dc60032c71c8c8d636b553f125b1f40cdc3e86846628773d16/{train,test}
for dir_path in $(gsutil ls "${GCS_PATH}/${directory}/"); do
  # Extract directory name from the path
  dir_name=$(basename "${dir_path}")
  echo "${directory}/${dir_name}"
  # Process each directory using the function
  process_directory "${directory}/${dir_name}"
done

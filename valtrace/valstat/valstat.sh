#!/bin/bash
BINARYPATH=/mnt/c/Users/27236/Desktop/binarycoverage_callgrind-main/valtest/test_func
TEMP_DIR="./tmp"
mkdir -p "$TEMP_DIR"

rm -rf "$TEMP_DIR/callannote.log"
rm -rf "$TEMP_DIR/callgrind.log"


for program in valgrind python3; do
  if ! command -v $program &> /dev/null; then
    echo "Please install $program to continue"
    exit 1
  fi
done

valgrind --tool=callgrind --trace-children=yes --callgrind-out-file="$TEMP_DIR/callgrind.log" $BINARYPATH 2> /dev/null
callgrind_annotate --tree=both "$TEMP_DIR/callgrind.log" > "$TEMP_DIR/callannote.log"
python3 funstat.py --binary $BINARYPATH --callgrindlogpath "$TEMP_DIR/callannote.log"
# rm -rf "$TEMP_DIR/callannote.log"
# rm -rf "$TEMP_DIR/callgrind.log"
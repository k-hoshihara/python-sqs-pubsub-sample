#!/bin/sh
FILE_PATH=$(jq -r '.tool_input.file_path')
if [ -s "$FILE_PATH" ] && [ "$(tail -c 1 "$FILE_PATH" | xxd -p)" != "0a" ]; then
  printf '\n' >> "$FILE_PATH"
fi

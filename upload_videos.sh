#!/bin/bash

set -u

REMOTE="${1:-gdrive:videos}"
TRANSFERS="${TRANSFERS:-4}"
CHUNK_SIZE="${CHUNK_SIZE:-64M}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-3}"

shopt -s nullglob
videos=(video_*.mp4)
shopt -u nullglob

if [ ${#videos[@]} -eq 0 ]; then
  echo "No files matching video_*.mp4 found in the current directory."
  exit 1
fi

# Natural sort: video_2.mp4 before video_10.mp4
IFS=$'\n' videos=($(printf '%s\n' "${videos[@]}" | sort -V))
unset IFS

total=${#videos[@]}
success=0
failed=0

for i in "${!videos[@]}"; do
  file="${videos[$i]}"
  num=$((i + 1))

  echo "[$num/$total] Uploading $file -> $REMOTE"

  attempt=1
  uploaded=0

  while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
    echo "  Attempt $attempt/$MAX_ATTEMPTS"

    if rclone copy "$file" "$REMOTE" \
      --transfers "$TRANSFERS" \
      --drive-chunk-size "$CHUNK_SIZE" \
      --fast-list \
      --progress; then
      uploaded=1
      break
    fi

    attempt=$((attempt + 1))
    if [ "$attempt" -le "$MAX_ATTEMPTS" ]; then
      echo "  Retry in 3 seconds..."
      sleep 3
    fi
  done

  if [ "$uploaded" -eq 1 ]; then
    echo "  Success: $file"
    success=$((success + 1))
  else
    echo "  Failed: $file"
    failed=$((failed + 1))
  fi

  echo
done

echo "Upload complete. Success: $success, Failed: $failed, Total: $total"

if [ "$failed" -gt 0 ]; then
  exit 2
fi

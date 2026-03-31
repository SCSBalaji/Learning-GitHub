#!/bin/bash

count=1

while IFS= read -r url; do
  [ -z "$url" ] && continue
  echo "Downloading video $count..."

  ffmpeg -nostdin -loglevel error \
  -i "$url" \
  -c copy \
  "video_$count.mp4"

  ((count++))
done < urls.txt

echo "All done!"
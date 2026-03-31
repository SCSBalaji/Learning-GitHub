chmod +x download.sh

chmod +x upload_videos.sh



./download.sh

./upload_videos.sh



ffmpeg -i "https://fast.wistia.com/embed/medias/a94t2ivslh.m3u8" -c copy video.mp4


rclone copy video_1.mp4 gdrive:videos \
--transfers 4 \
--drive-chunk-size 64M \
--fast-list \
--progress


whisper video_5.mp4 --model small --fp16 False --language English
// English only. It is translating it
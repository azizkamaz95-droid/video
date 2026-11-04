#!/bin/bash
# Colle la miniature choisie en toute premiere image de la video (les reseaux prennent souvent la 1re image comme couverture).
# usage: add_cover.sh <video_master.mp4> <miniature.jpg> <sortie.mp4> [nb_images=3]
# 3 images a 30 i/s = 0,1 s. Du silence de meme duree est ajoute au son : rien ne se decale.
set -e
V="$1"; T="$2"; O="$3"; N="${4:-3}"
DUR=$(python3 -c "print($N/30)")
ffmpeg -v error -y -loop 1 -framerate 30 -t "$DUR" -i "$T" -f lavfi -t "$DUR" -i anullsrc=r=48000:cl=stereo -i "$V" \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p[c];[2:v]setsar=1,fps=30,format=yuv420p[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[sa];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[ma];[c][sa][v][ma]concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" -c:v libx264 -preset medium -crf 17 -c:a aac -b:a 256k -movflags +faststart "$O"
echo "cover ajoutee : $O ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$O") s)"

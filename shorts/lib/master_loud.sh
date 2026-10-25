#!/bin/bash
# Phone-friendly master: louder (-10.5 LUFS target), clearer voice, bass of the music made audible on small speakers
# (harmonics of the < 160 Hz band). usage: master_loud.sh <episode_dir> <video_in> <video_out>
set -e
EP=$1; IN=$2; OUT=$3; T=$(mktemp -d)
ffmpeg -v error -y -i $EP/assets/voice/voice.wav -i $EP/assets/audio/music.wav -i $EP/assets/audio/sfx.wav -filter_complex "
[0:a]aformat=channel_layouts=stereo,highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=3.5,equalizer=f=200:t=q:w=1:g=-2,acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=2[v];
[1:a]asplit=2[md][mh];[mh]lowpass=f=160,volume=14dB,asoftclip=type=tanh,highpass=f=220,highpass=f=220,lowpass=f=900,volume=-2dB[h];
[md][h]amix=inputs=2:normalize=0,volume=4dB[m];[v][m][2:a]amix=inputs=3:normalize=0[mix]" -map "[mix]" -ar 48000 $T/raw.wav
I=$(ffmpeg -i $T/raw.wav -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-10.5-($I),2))")
ffmpeg -v error -y -i $T/raw.wav -af "volume=${G}dB,alimiter=limit=0.72:attack=2:release=60:level=false" $T/mix.wav
ffmpeg -v error -y -i $IN -i $T/mix.wav -map 0:v -map 1:a -c:v libx264 -b:v 5000k -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart $OUT
rm -rf $T
ffmpeg -i $OUT -vn -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2

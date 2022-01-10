#!/bin/bash

read SEED length <<<$(SEED=${SEED} python3 bandersnatch.py)
echo $length >&2

ffmpeg -hide_banner -v warning -stats -f concat -safe 0 -i out/${SEED}.txt -c copy -movflags +faststart out/${SEED}.mp4
echo out/${SEED}.mp4

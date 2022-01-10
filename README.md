bandersnatch
============

In 2019 I watched Black Mirror: Bandersnatch on Netflix. Immediately I wanted to find out how this choose-your-own-adventure fourth-wall-breaking movie worked, so I decided to make a tool to use the movie's two data files (SegmentMap.json and bandersnatch.json) to generate a full playthrough, reimplementing all logic, to produce standalone video files containing a possible version of the movie someone might see. I made this tool overnight while drinking and livestreaming, and then forgot about it for two years. Now, I've taken that code, fixed it up, made it possible to re-generate the same movie using a seed integer, and I'm planning on making a web service for this tool as well.

Files
-----
* make.sh : The main entry point. A script that uses bandersnatch.py to generate a playthrough, using either a provided SEED environment variable or generating one if none is provided. SEED must be an integer; it then calls ffmpeg to concatenate the required segments into the output file. The output filename is returned on stdout after ffmpeg is complete. The estimated file length is shown on stderr.

* SegmentMap.json / bandersnatch.json : Data files, apparently originally from Netflix's video player. I don't have source URLs for these yet
* state\_descriptions.json : A list I'm working on, notating what each internal state flag indicates. Used when DEBUG is set when running bandersnatch.py
* generate\_segment\_shell.py : A script that takes the SegmentMap.json and Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mp4 (which is a 5:12:14 video file containing all segments from Bandersnatch; the x265 version is NOT compatible) and produces a shell script containing ffmpeg lines to encode segments from the source video. Pipe the output of this script to bash after running it once to make sure it works
* bandersnatch.py : The core of the project, iterates through the game starting from segment 1A, tracking state flags, following respawns, and exiting cleanly when the game reaches one of the four credits segments, closing with the netflix ident. Writes a file to out/$SEED.txt containing ffmpeg concat syntax for building the movie

Not included
------------
* Black Mirror: Bandersnatch. It would be illegal to provide a copy of the movie, and also impossible to recreate the experience of watching the movie due to its interactive elements. There is a collection of all segments from the movie that is required for this project, which can be found by googling B647A9BC9D3E2445B31175293A96C9979BD2F5FD, but that also doesn't recreate the experience of watching the movie. Neither does this project. Just go get a Netflix subscription and watch Bandersnatch. Then, if you're as intrigued by the concept as I was, come back and check out this project.
* The segments of Bandersnatch. They contain copyrighted material. You can create these yourself after acquiring Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mp4.
* Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mp4. The file in the torrent was an mkv containing, primarily, the Spanish dub of the film, with the English dub as a secondary audio track. I produced an English version without the extra metadata with `ffmpeg -i Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mkv -map_metadata -1 -map 0:0 -map 0:2 -c copy Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mp4`, then moved the generated file to this working directory.

Franck.py

Get video details (title, formats, etc) of a Jeuxvideo.com video from its URL.

API running on Flask, simple front-end.

francky.py and get_gl.sh help download a video directly from the cli

usage:

python francky.py http://PAGEWITHAVIDEOINSIDE
returns a wget formatted url to download the highest quality format

sh francky.sh http://PAGEWITHAVIDEOINSIDE download the video to a preset download folder

can be parallelized with GNU parallel (or other):
parallel -a FILEWITHURLSINSIDE francky.sh

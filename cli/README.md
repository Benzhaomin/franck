# Usage

usage: franck-cli.py [-h] [--log LOGLEVEL] [--quality QUALITY] url [url ...]

positional arguments:
  url                url of a video or video list page

optional arguments:
  -h, --help         show this help message and exit
  --log LOGLEVEL
  --quality QUALITY

# Output

One video per line: title\turl\n

## Example

$ python franck-cli.py --quality=1080p  'http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=300'

The Elder Scrolls IV : Oblivion : Grotte et Quête http://videohd.jeuxvideo.com/200603/oblivion_grotte_et_quete-00000085-high.mp4
The Elder Scrolls IV : Oblivion : Cité Impériale  http://videohd.jeuxvideo.com/200603/oblivion_cite_imperiale-00000086-high.mp4
[...]

Note that the requested quality wasn't available for those videos so the best one was selected instead.

To only get the video url, pipe into `cut -f 2`

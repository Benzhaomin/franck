# API

## Usage

usage: franck-http [-h] [--log LOGLEVEL] [--host HOST] [--port PORT]

optional arguments:
  -h, --help      show this help message and exit
  --log LOGLEVEL  output log message of this level and up (default: WARNING)
  --host HOST     hostname or ip address (default: localhost)
  --port PORT     port number (default: 8080)

## Request

```curl http://localhost:8080/video/<path>```
```curl http://localhost:8080/videos/<path>```

## Video json format

```
{
  'id': video_id,
  'url': url of the video's page,
  'cover': url of the video's thumbnail,
  'title': title,
  'description': description,
  'sources': {
    '<ratio>': {
      'file': url of the video file,
      'size': 0
  },
  'timeline': absolute url of the video's timeline (grid of thumbnails),
  'iframe':  absolute url of the video's iframe embed,
}
```

## /video/<video_page>

Get a single Video object from its URL.

## /videos/<video_page>

Get a list of Video objects from a page containing a list of links to video pages.

# Website

The front-end is a simple HTML page that does an AJAX request to the JSON API.

## Running

Simply serve index.html with any server. Using Python 3's http server:

```
cd http/html/
python -m http.server > ../web.log 2>&1 &
```

## Usage

- load the page, when using the server above: ```sensible-browser http://localhost:8000/```
- either paste an URL or use one of the presets on the right, click go
- click on a quality to display the video inline in the page using a <video> player, no ads

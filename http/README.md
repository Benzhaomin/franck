# Running

```franck-http --log=DEBUG```

# Request

```curl http://localhost:8080/video/<path>```
```curl http://localhost:8080/videos/<path>```

# API

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

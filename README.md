# STREAKY
Unofficial and completely amatorial api client to get and set data from your Streak©.
See more on the [Streak© site](https://www.streak.com/) and [Streak© api](https://streak.readme.io/docs/overview).


## Installation

```bash
pip install streaky
```

## Usage

```python
import streaky as sr

automa = sr.Auth(r"my_api_key.txt")
pipeline = automa.pipeline("MY PIPELINE")
box = automa.box(pipeline, "MY BOX NAME")

```

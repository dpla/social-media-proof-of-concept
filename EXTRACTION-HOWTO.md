# Extracting and working with web archives

If you archived a web page according to the "from the command line" [CAPTURING-HOWTO](CAPTURING-HOWTO.md) guide, you should end up with a directory named `crawls` that contains two subfolders:

- The `profiles` directory contains the login credentials that you stored when you logged in to TikTok in Browsertrix. This is only useful for additional capture sessions.

- The `collections` directory contains a series of subfolders, one for each time you ran a Browsertrix capture.

Inside each subfolder of `collections`, you'll find a few files:

- a `.wacz` file that is optimized for playing back in a browser. One way to think of this file is as a specially-crafted `.zip` file that contains the rest of the files in this crawl directory. The easiest way to get started with this file is to navigate to [replayweb.page](https://replayweb.page/) and load the file in the file chooser. The resulting UI will allow you to see all the individual files that were captured as part of the web archiving process, but more importantly, you'll be able to "play back" the web archive as if it were a live web page.

- A directory called `pages`. Inside this folder are two [JSON Lines](https://jsonlines.org/) files that contain metadata about the page that was captured.

- A directory called `logs` that contains the information that was logged during the capture process.

- An `archive` directory that contains two [WARC](<https://en.wikipedia.org/wiki/WARC_(file_format)>) (web archive) files.

The WARC with the `text` prefix contains the text that was scraped out of the page after the comments were loaded. You can see the contents by running a command like:

> gzcat text-20240814180920377.warc.gz

The other WARC, which begins with the label `rec`, contains the data captured from the web session.

The included [extraction.py](extraction.py) script can extract a video file from the WARC. It does this by cycling through the .mp4 entries in the WARC and saving them out as independent video files. Generally speaking,

ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 2 output.wav

./main -m /Users/michael/github/whisper.cpp/models/ggml-large-v3.bin -f ~/crawls/collections/crawl-20240814180624500/archive/output.wav

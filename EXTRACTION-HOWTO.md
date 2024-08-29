# Extracting and working with web archives

Note: This guide assumes you're using a Mac or a Linux system, and are relatively familiar with the command line and installing command line software.

The intent is to show the technical feasibility of using web archiving as the primary source asset for an archive of TikTok posts. We'll step through how to extract assets from the archive in order to serve search, discovery, and access use cases.

## Contents of the `crawls` directory

If you archived a web page according to the "from the command line" [CAPTURING-HOWTO](CAPTURING-HOWTO.md) guide, you should end up with a directory named `crawls` that contains two subfolders:

- The `profiles` directory contains the login credentials that you stored when you logged in to TikTok in Browsertrix. This is only useful for additional capture sessions.

- The `collections` directory contains a series of subfolders, one for each time you ran a Browsertrix capture.

Inside each subfolder of `collections`, you'll find a few files:

- a `.wacz` file that is optimized for playing back in a browser. One way to think of this file is as a specially-crafted `.zip` file that contains the rest of the files in this crawl directory. The easiest way to get started with this file is to navigate to [replayweb.page](https://replayweb.page/) and load the file in the file chooser. The resulting UI will allow you to see all the individual files that were captured as part of the web archiving process, but more importantly, you'll be able to "play back" the web archive as if it were a live web page.

- A directory called `pages`. Inside this folder are two [JSON Lines](https://jsonlines.org/) files that contain metadata about the page that was captured.

- A directory called `logs` that contains the information that was logged during the capture process.

- An `archive` directory that contains two [WARC](<https://en.wikipedia.org/wiki/WARC_(file_format)>) (web archive) files.

## Extracting text and video

In the `archive` directory, the WARC with the `text` prefix contains the text that was scraped out of the page after the comments were loaded. You can see the contents by running a command like:

> gzcat text-20240814180920377.warc.gz

The other WARC, which begins with the label `rec`, contains the data captured from the web session.

The included [extraction.py](extraction.py) script can extract a video file from the WARC. It does this by cycling through the .mp4 entries in the WARC and saving them out as independent video files. The video extraction script requires that `warcio` is installed, you can do so by running `pip install warcio` or `pip3 install warcio` in your preferred python environment.

Once you've installed `warcio`, you can run the script on the WARC you've generated:

> python extraction.py <input.warc> <output.mp4>

Your <input.warc> will be the warc prefixed by `rec-` in the `crawls/collections/crawl-datetime/archive` directory. It is convenient to save the `output.mp4` in the same directory.

## Creating a transcript for search indexing

The next step is to extract the audio track of the video for transcription. Install `ffmpeg` and use the `mp4` you've just created to run a command like:

> ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 2 output.wav

It is convenient to save the `output.wav` in the same `archive` directory as the other files.

Next, we'll get a transcript based on this audio track. We're using `Whisper.cpp` because it supports GPUs on ARM Macs with zero configuration or setup, which greatly speeds transcription. Download [whisper.cpp](https://github.com/ggerganov/whisper.cpp) via `git clone https://github.com/ggerganov/whisper.cpp.git`, change into that project directory, and run these commands to set it up:

> make
> bash ./models/download-ggml-model.sh base

`Whisper.cpp` is ready to run. The following command will generate a transcript from the audio (edit the path to the .wav file to match yours):

> ./main -m models/ggml-large-v3.bin -f ~/crawls/collections/crawl-20240814180624500/archive/output.wav

This will print the output to the console as part of the logging output, but using the switch `-oj` will write a .json file with the content to the same folder as the .wav. There are more formatting options you can peruse with the `-h` switch.

## Conclusion

With techniques like these, it is easy to envision how an archive of TikToks that were collected using web archiving tools could be the primary asset in a repository that allowed for a number of secondary use cases, such as:

- Viewing the posts in an embedded WACZ viewer.
- Playing the video in a player outside the primary interface.
- Searching and discovering posts via transcriptions of the audio or keywords in comments.
- Performing analytical workflows on the transcriptions and comments to discover trends.

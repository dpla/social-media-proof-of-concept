# Social Media Repository Proof of Concept

This is a collection of information that DPLA has collated from investigations related to a series of grants from Netgain Partners and the Sloan Foundation about how libraries could play a role in social media research by archiving posts for later use.

## Why web archives?

While many types of web scraping are adequate for preserving social media posts in some form, the modern practice of web archiving has benefits that should be considered, particularly from the point of view of a library, archive, or museum considering this work.

The biggest benefit to using a modern web archiving stack to preserve social media posts is that one can do as much as possible to preserve the overall context and user experience of the social media post at the point of capture.

Even though scraping the video, photo, and textural content that constitutes the body of the post helps future generations understand the main "text" of the post, future viewers may want to study the context in which the post was presented. Ephemera like related posts, comments, or even the graphical presentation of the post may be relevant for future study. Using a facility for capturing these posts that preserves as much as possible the contemporaneous experience of interacting with the web site makes these alternate modes of inquiry possible.

## What are web archives?

A web archive is a specially-formatted concatenation of the data that a web browser sees as it loads web pages. The most visible place that uses web archives is the Wayback Machine hosted by the Internet Archive, although other projects make use of web archives as well, in particular, [Conifer](https://conifer.rhizome.org/), a project by [Rhizome](https://rhizome.org); [Perma.cc](https://perma.cc), a citation tool operated by the Harvard Library Innovation Lab; and the [Webrecorder](https://webrecorder.net) project.

These archives allow for "playback," a simulation of the experience of viewing the original page in a web browser. Depending on the capture technique, these playback experiences can seem indistinguishable from actually browsing the site. Video controls will continue to work, and interactive features like unfurls can continue to work.

Modern web archives are stored in a ISO-standardized file type called [WARC](<https://en.wikipedia.org/wiki/WARC_(file_format)>), or a new variant called [WACZ](https://webrecorder.net/2021/01/18/wacz-format-1-0.html), which makes WARC files more efficient to playback. The important thing to know is that everything required to recreate the experience of browsing the page (or pages) in the web archive is encapsulated in a single file that you can treat like any other document on your computer, or host on the web.

## Capturing

A howto for using web archiving tools to capture social media posts, including those that use video, is available in [CAPTURING-HOWTO.md](CAPTURING-HOWTO.md). Our initial proof of concept is for TikTok video pages, however, the same
tools and practices can be used on other social media sites as well.

## Playback

Once you have a collection of web archives and want to present them to users, you need a playback mechanism to show them in a browser. One such mechanism is [Replay Webpage](https://replayweb.page/), which is part of the Webrecorder suite of tools.

## Extraction

We've demoed some scripts for extracting information from web archives in [EXTRACTION-HOWTO.md](EXTRACTION-HOWTO.md).

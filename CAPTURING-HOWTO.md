# How to capture a TikTok post using Browsertrix crawler

There are many different tools available that create web archives, but currently, the [Browsertrix](https://browsertrix.com/) suite has the most affordances for capturing social media posts. Chiefly among these:

1. A suite of custom scripts to aid compatibility with social media sites and facilitate captures called [Browsertrix Behaviors](https://github.com/webrecorder/browsertrix-behaviors). In the case of TikTok, Browsertrix Behaviors knows how to automatically expand comment threads and load additional comments beyond what shows in the browser when a video loads.

2. A facility for logging in an automated browser so that CAPTCHAs can be prevented.

3. A browser plugin that allows someone to create a web archive without any expertise in running web archiving software.

Worth noting is the [Scoop](https://github.com/harvard-lil/scoop) project from the [Harvard Library Innovation Lab](https://lil.law.harvard.edu/), which previously was deployed in an experimental capacity for archiving Twitter/X posts. However, the current primary use case for this software does not require facilitating site logins, and without that, it can be difficult to evade CAPTCHAs on tiktok.com.

## Performing a web capture

### ... in a browser

1. In a Chrome-based browser, add the [Webrecorder ArchiveWeb.page Extension](https://chromewebstore.google.com/detail/webrecorder-archivewebpag/fpeoodllldobpkbkabpblcfaogecpndd).
2. Browse to [TikTok](https://tiktok.com) and log in normally. Complete any CAPTCHA that appears. You can also collect a limited amount of data without first logging in.
3. Navigate to a video page you'd like to archive.
4. In the Extensions button next to the URL bar, click on Webrecorder ArchiveWeb.page extension, check the Autopilot checkbox, and then click Start Archiving.
5. You will observe the extension automatically playing the video, as well as automatically scrolling the web page down to allow content to be loaded into view. Additionally, the autopilot feature will automatically unfurl the comment threads so they are recorded as well.
6. Technically, the recording process can be interrupted at any time, however, you most likely will want to allow all the content to load first.
7. Once the browser stops loading the comments, click the Stop Archiving button.
8. To view your captures, you can click the Home icon on the browser extension. From this page, you can download your session.

### ... from the command line

Setting up captures from the the command line is a two-step process. First, you

0. Install [Docker](https://docs.docker.com/engine/install/) or [Docker Desktop](https://www.docker.com/products/docker-desktop/), depending on your platform.

#### Creating a browser profile

1. Run the following command into a terminal window:
   > docker run -p 6080:6080 -p 9223:9223 -v $PWD/crawls/profiles:/crawls/profiles/ -it webrecorder/browsertrix-crawler create-login-profile --url [URL of a TikTok video page]

Docker will download the Browsertrix image before running it, which will take a few minutes. You'll know this is done when you see output similar to the following:

`{"timestamp":"2024-08-13T16:54:33.537Z","logLevel":"info","context":"general","message":"Loaded!","details":{}}`

It's important to use the URL of an actual TikTok video page, to ensure you trigger any CAPTCHAs that may be presented, so you can solve them while Browsertrix is watching.

2. Browse to [http://localhost:9223/](http://localhost:9223/) on a Chromium-based browser, complete any CAPTCHA that appears, and login in the web streaming interface that appears in the web page.

3. Click Create Profile.

This process saves a login session in a cookie that Browsertrix will be able to access later. You should only need to do steps 1-3 periodically if you are logged out from the Tiktok website.

#### Capturing a page

Once you have a login set up, the following command will capture a TikTok video:

> docker run -p 9999:9999 -v $PWD/crawls/profiles:/crawls/profiles -v $PWD/crawls:/crawls/ -it webrecorder/browsertrix-crawler crawl --url <URL OF VIDEO PAGE> --scopeType page --generateWACZ --screencastPort 9999 --profile /crawls/profiles/profile.tar.gz --behaviorTimeout 6000 --text final-to-warc`

It's convenient to keep an eye on the archiving process by opening `localhost:9999` because then you will be able to recognize any CAPTCHAs that appear. Note the capture may not capture all comments on a clip if there are more than a certain number, although it will certainly do up to several hundred.

Here's an explanation of what those arguments mean:

- `-p 9999:9999`: This tells the Docker daemon to expose port 9999 in the Docker container to the host. This is important if you want to watch the archiving process happen, which works in conjunction with the `--screencastPort` parameter.

- `-v $PWD/crawls/profiles:/crawls/profiles` This mounts the profiles directory in the Docker container so Browsertrix can load the profile you created in Creating a browser profile.

- `-v $PWD/crawls:/crawls/` This mounts the overall crawls directory in the Docker container so Browsertrix can save the web archives somewhere that lives beyond the lifetime of the container.

- `-it` This performs some technical configuration of the Docker daemon to allow Browsertrix to run correctly.

- `webrecorder/browsertrix-crawler` This is the Docker image that contains the Browsertrix software. Docker will download this from Docker Hub.

- `crawl` This command tells the software we're trying to perform a crawl, which means to capture one or more web pages. We'll be confining the crawl to one page in other arguments.

- `--url` Allows us to specify the URL we wish to crawl.

- `--scopeType page` Tells Browsertrix we only want to crawl a single page, rather than continuing to follow the links on this page onward to other pages.

- `--generateWACZ` A WACZ is a Zip file-based, indexed version of a Web archive that is easier to play back later.

- `--screencastPort 9999` If you direct your browser to [http://localhost:9999](http://localhost:9999) while the capturing is happening, you'll be able to watch the Browsertrix engine at work, expanding the comments and scrolling the page. This can also be helpful for diagnosing things when things go wrong. A typical thing to watch for is either the login expired, or the UI is presenting a CAPTCHA.

- `--profile /crawls/profiles/profile.tar.gz` This tells Browsertrix where to find the login information you saved will show up in the Docker container.

- `--behaviorTimeout 6000` This gives Browsertrix a very long time to expand all the comments on the page and save them to the archive (100 minutes). Setting this to an arbitrarily large number like this just ensures it can collect whatever there are. If there are few comments, it will complete sooner. If you rather not wait around for comments, you can reduce this number, and Browsertrix will collect what comments it can in the time given.

- `--text final-to-warc` This tells Browsertrix to save all the text on the page (including the comments) at the end of the capture process to a file in the archive.

Browsertrix is also available as a hosted service at [browsertrix.com](https://browsertrix.com/).

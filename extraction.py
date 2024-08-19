from warcio.archiveiterator import ArchiveIterator
import sys
from pathlib import PurePath

if len(sys.argv) != 3:
    print("Usage: python extraction.py <input.warc> <output.mp4>")
    sys.exit(1)

count = 0

with open(sys.argv[1], "rb") as stream:
    for record in ArchiveIterator(stream):
        if record.rec_type == "response":
            if (
                record.http_headers
                and record.http_headers.get_header("Content-Type") == "video/mp4"
            ):
                path = PurePath(sys.argv[2])

                if count > 0:
                    path = path.with_stem(f"{path.stem}_{count}")

                with open(path, "wb") as output_stream:
                    output_stream.write(record.content_stream().read())

                count += 1

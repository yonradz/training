import os
import sys

SNIPPET_DIR = 'snippets/'
HOSTNAME = 'n9k1'

FAILURE = 1
SUCCESS = 0

for snippet_file in os.listdir(SNIPPET_DIR):
    with open(os.path.join(SNIPPET_DIR, snippet_file)) as snippet_file_handler:
        file_contents = snippet_file_handler.read()
        if ('hostname ' + HOSTNAME) not in file_contents:
            sys.exit(FAILURE)


sys.exit(SUCCESS)
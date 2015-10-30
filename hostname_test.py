import os
import sys

SNIPPET_DIR = 'snippets/'
HOSTNAME = 'n9k1'

FAILURE = 1
SUCCESS = 0

# Iterate over all files in the snippets directory
for snippet_file in os.listdir(SNIPPET_DIR):
    
    # Open each file so its contents can be read
    with open(os.path.join(SNIPPET_DIR, snippet_file)) as snippet_file_handler:
        
        # Load the contents of each file into the variable file_contents
        file_contents = snippet_file_handler.read()
        
        # If 'hostname n9k1' isn't in each file, the test fails
        if ('hostname ' + HOSTNAME) not in file_contents:
            sys.exit(FAILURE)

# If after iterating through all files, no file has failed, the test succeeds.
sys.exit(SUCCESS)

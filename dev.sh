#!/bin/bash
# Clean the _site directory and run the embedded dev server (port 4000)
rm -r _site
jekyll serve --watch

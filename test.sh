#!/bin/bash
#
# Run the tests
# 
bundle exec jekyll build --drafts
grunt test
bundle exec htmlproof ./_site
rspec

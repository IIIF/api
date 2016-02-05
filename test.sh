#!/bin/bash
#
# Run the tests
#

set -ev # This makes this script exit as soon as any command exits with >0

bundle exec jekyll build --drafts
grunt test
bundle exec htmlproof ./_site
rspec

#!/bin/bash
#
# Run the tests
#

# make this script exit as soon as any command exits with >0
set -ev

# Without this, deleted pages will stick around in the next build
rm -rf ./_site

# Build the site with draft news posts
bundle exec jekyll build --drafts

grunt test
bundle exec rake test

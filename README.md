[![Stories in Ready](https://badge.waffle.io/IIIF/iiif.io.png?label=ready&title=Ready)](https://waffle.io/IIIF/iiif.io)
[![Build Status](https://travis-ci.org/IIIF/iiif.io.svg?branch=master)](https://travis-ci.org/IIIF/iiif.io)

# Specifications

Markdown Source of specifications documents

## To Debug the Site

 1. `bundle install`

 2. Run `$ ./dev.sh` to compile the site and run a dev server on [http://localhost:4000](http://localhost:4000).

## To Publish the Site

(E.g. for Apache to serve), run `./publish.sh /my/site/dir`. Note that if the site is not at '/' on the server, js and css will not work (the source files use absolute paths.)

## Some Things to Note

 * Much of the site data is in the YAML files in `_data/` (e.g. member institutions, server impls, demos, etc.) make edits there.
 * The latest versions of the APIs are set in `_config.yml`. Change there will get pushed to `.htaccess`, `technical-details/`, and any other links.
 * Always use the \[link text\]\[ref\] method of creating links.  `ref` must consist only of a-zA-Z0-9_- and the first character must be a-zA-Z
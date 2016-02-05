[![Stories in Ready](https://badge.waffle.io/IIIF/iiif.io.png?label=ready&title=Ready)](https://waffle.io/IIIF/iiif.io)
[![Build Status](https://travis-ci.org/IIIF/iiif.io.svg?branch=master)](https://travis-ci.org/IIIF/iiif.io)

# Specifications

Markdown Source of specifications documents

## To Debug the Site

 1. `bundle install`

 2. Run `rake dev` to compile the site and run a dev server on [http://localhost:4000](http://localhost:4000).

## To Run the Tests

```
rake ci
```

## To Publish the Site to iiif.io

We now use Capistrano to deploy the site.

```
bundle exec cap production deploy
```

Will deploy to the iiif.io site if you have permission.

## Some Things to Note

 * Much of the site data is in the YAML files in `_data/` (e.g. member institutions, server impls, demos, etc.) make edits there.
 * The latest versions of the APIs are set in `_config.yml`. Change there will get pushed to `.htaccess`, `technical-details/`, and any other links.
 * Always use the \[link text\]\[ref\] method of creating links.  `ref` must consist only of a-zA-Z0-9_- and the first character must be a-zA-Z

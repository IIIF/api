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

Commits to `github.com/iiif/iiif.io` will automatically be deployed to `iiif.io` using a link with AWS S3.

## Some Things to Note

 * Much of the site data is in the YAML files in `_data/` (e.g. member institutions, server impls, demos, etc.) make edits there.
 * The latest versions of the APIs are set in `_config.yml`. Change there will get pushed to `.htaccess`, `technical-details/`, and any other links.
 * The website is now split with the root website living in [iiif/root-website](https://github.com/IIIF/iiif-root-website). This repo contains the specifications in `/api/` and `/model/`. Links internal and external should be in the following forms:
    * Internal relative link `[hyperlink text]({{ site.url }}{{ site.baseurl }}/end/point)`
    * link to root website from api website (not relative to this repo) `[hyperlink text]({{ page.webprefix }}/end/point)`
    * External link `[anchor-text](http://example.com/end/point)`
    * Reference link `[text][link_name]` where link_name is expanded at the bottom of the page.
 * If this branch has a domain name associated with it e.g. prezi3.iiif.io then add the name of the branch to the `ROOT_BRANCHES` variable in the `.travis.yml`. Note branch names are sperated by a space.    

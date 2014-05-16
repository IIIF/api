#!/bin/bash
# Publish the site to a directory.
#
# WARNING: Script DELETEs and replaces the contents of the supplied directory
# path. Be careful where you point it!
#
# Usage: ./publish.sh /var/www/mysite

dir=$1

if [ $dir"X" == "X" ]; then
     echo -ne "Supply a destination directory for the site, e.g. ./publish.sh "
     echo "/var/www/mysite"  1>&2
     exit 64
fi

jekyll build -d $dir

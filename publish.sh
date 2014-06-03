#!/bin/bash
# Publish the site to a directory.
#
# WARNING: Script DELETEs and replaces the contents of the supplied directory 
# path. Be careful where you point it!
#
# Usage: ./publish.sh /var/www/mysite

export PATH="/usr/local/rvm/gems/ruby-2.1.2/bin:/usr/local/rvm/gems/ruby-2.1.2@global/bin:/usr/local/rvm/rubies/ruby-2.1.2/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/rvm/bin:/home/iiif/bin"
export rvm_bin_path="/usr/local/rvm/bin"
export GEM_HOME="/usr/local/rvm/gems/ruby-2.1.2"
export IRBRC="/usr/local/rvm/rubies/ruby-2.1.2/.irbrc"
export MY_RUBY_HOME="/usr/local/rvm/rubies/ruby-2.1.2"
export rvm_path="/usr/local/rvm"
export rvm_prefix="/usr/local"
export GEM_PATH="/usr/local/rvm/gems/ruby-2.1.2:/usr/local/rvm/gems/ruby-2.1.2@global"1
export rvm_version="1.25.27 (stable)"

dir=$1

if [ $dir"X" == "X" ]; then
     echo -ne "Supply a destination directory for the site, e.g. ./publish.sh "
     echo "/var/www/mysite"  1>&2
     exit 64
fi

if [ -d $dir ]; then
  rm -rf $dir/*
fi
./myjekyll build -d $dir
#jekyll build -d $dir

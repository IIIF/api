#!/bin/bash

HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SOURCE=$HERE/../source
OUT=$SOURCE/robots.txt

cd $SOURCE
echo "User-agent: *" > $OUT
echo "Sitemap: http://iiif.io/sitemap.xml" >> $OUT
for path in `grep -r "sitemap: false" | awk -F':' '{print $1}'`; do
  echo -n "Disallow: /" >> $OUT
  echo $path | sed -r -e 's/(index.html)|(index.md)//' | sed -e 's|.html|/|' >> $OUT
done

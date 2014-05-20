# Derived  from https://github.com/kogakure/jekyll-plugin-abbr
#
# Original license follows:
#
# ~~~~~
# The MIT License
# Copyright (c) 2012 Stefan Imhoff
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ~~~~~~

# Just using Liquid, e.g.:
#
   # {% for acronym in site.data.acronyms %}
   #   {% assign short = acronym[0] %}
   #   {% capture open %}<abbr title="{{ acronym[1] }}">{% endcapture %}
   #   {% assign close = '</abbr>' %}
   #   {% assign markup = short | prepend: open | append: close %}
   #   {% assign content = content | replace: short, markup %} 
   # {% endfor %}
#
# Wraps instances in title and alt attributes as well, so a smarter filter
# is necessary...

ACRONYMS_FILE = 'acronyms.yml' # in _data

require 'yaml'

module Jekyll
  module AbbreviationFilter
    def abbr(input)
      data = File.expand_path("../../_data/#{ACRONYMS_FILE}", __FILE__)
      abbr_dict = YAML.load(File.open(data))
      abbr_dict.each do |abbr, title|
        input.gsub! /\b#{abbr}\b(?![^">]+">|<\/abbr>|">)/, "<abbr title=\"#{title}\">#{abbr}</abbr>"
      end
      input

    end
  end
end

Liquid::Template.register_filter(Jekyll::AbbreviationFilter)

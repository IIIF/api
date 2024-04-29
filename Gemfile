source 'https://rubygems.org'

gem 'jekyll', '~> 4.1.1'

# for local development, clone theme + use path loader
# gem 'iiifc-theme', path: 'iiifc-theme'
gem 'iiifc-theme', github: 'iiif/iiifc-theme', branch: 'main'

gem 'jekyll-redirect-from'
gem 'jekyll-seo-tag'

# A Fix
gem 'webrick', "~> 1.7"

# Note 0.0.3 is broken due to: https://github.com/gemfarmer/jekyll-liquify/issues/8
gem "jekyll-liquify", "0.0.2"

group :development, :test do
  gem 'html-proofer', "3.19.0"
  gem 'rspec'
end

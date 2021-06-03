source 'https://rubygems.org'

gem 'jekyll', '~> 4.1.1'

# for local development, clone theme + use path loader
# gem 'iiifc-theme', path: 'iiifc-theme'
gem 'iiifc-theme', github: 'mnyrop/iiifc-theme', branch: 'main'

group :jekyll_plugins do
  gem 'jekyll-redirect-from'
  gem 'jekyll-sitemap'
  gem 'jekyll-gzip'
end

group :development, :test do
  gem 'html-proofer'
  gem 'rspec'
  gem 'rake'
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

require 'html-proofer'
require 'rspec/core/rake_task'

RSpec::Core::RakeTask.new(:spec)

SITE_DIR = './_site'

def jekyll(cmd)
  sh "bundle exec jekyll #{cmd}"
end

def build_site
  jekyll 'clean'
  jekyll "build -d _site/test --baseurl /test"
end

desc 'Run the Markdown specs and HTML Proofer'
task :ci do
  build_site
  sh 'grunt test'
  sh 'scripts/check_json.py -v'
  sh 'scripts/check_mixedcontent.sh'
  Rake::Task['spec'].invoke
  Rake::Task['check_html'].invoke
end

desc 'Check all links and cache the results'
task :check_html do
  HTMLProofer.check_directory(SITE_DIR, {
    cache: { timeframe: '1w' },
	 check_html: true,
	 http_status_ignore: [0, 301, 302],
   url_ignore: [
     /.*\/(about|technical-details|apps|demos|event|news|community|stanford\.edu|)/,
   ]
  }).run
end

desc 'Run the site locally on localhost:4000'
task :dev do
  sh 'bundle exec jekyll clean'
  sh 'bundle exec jekyll build'
  sh 'bundle exec jekyll serve --watch --drafts'
end

task default: :ci

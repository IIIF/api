require 'html-proofer'
require 'rspec/core/rake_task'

RSpec::Core::RakeTask.new(:spec)

SITE_DIR = './_site'

def jekyll(cmd)
  sh "bundle exec jekyll #{cmd}"
end

def build_site
  jekyll 'clean'
  jekyll 'build'
end

'Run the Markdown specs and HTML Proofer'
task :ci do
  build_site
  sh 'grunt test'
  sh 'scripts/check_json.py -v'
  Rake::Task['spec'].invoke
  Rake::Task['check_internal_links'].invoke
end

'Check internal links only without caching'
task :check_internal_links do
  HTMLProofer.check_directory(SITE_DIR, {
    disable_external: true
  }).run
end

'Check all links and cache the results'
task :check_all_links do
  HTMLProofer.check_directory(SITE_DIR, {
    cache: { timeframe: '1w' }
  }).run
end


'Run the site locally on localhost:4000'
task :dev do
  build_site
  jekyll 'serve --watch --drafts'
end

task default: :ci

require 'html/proofer'
require 'rspec/core/rake_task'

RSpec::Core::RakeTask.new(:spec)

def rebuild
  sh 'rm -rf ./_site' if Dir.exists?('./_site')
  sh 'bundle exec jekyll build'
end

'Run the Markdown specs and HTML Proofer'
task :ci do
  rebuild
  sh 'grunt test'
  Rake::Task['spec'].invoke
  HTML::Proofer.new('./_site', cache: { timeframe: '2w' } ).run
end

'Run the site locally on localhost:4000'
task :dev do
  rebuild
  sh 'rm -rf ./_site' if Dir.exists?('./_site')
  sh 'jekyll serve --watch --drafts'
end

task default: :ci

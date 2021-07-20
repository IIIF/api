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
  #sh 'scripts/check_json.py -v'
  Rake::Task['spec'].invoke
  Rake::Task['check_html'].invoke
end

desc 'Check all links and cache the results'
task :check_html do
  HTMLProofer.check_directory(SITE_DIR, check_html: true,
                                         validation: {report_mismatched_tags:true, report_invalid_tags: true },
                                         disable_external: true,
                                         checks_to_ignore: ['LinkCheck']
                                         ).run
end

desc 'Run the site locally on localhost:4000'
task :dev do
  sh 'bundle exec jekyll clean'
  sh 'bundle exec jekyll build'
  sh 'bundle exec jekyll serve --watch --drafts'
end

task default: :ci

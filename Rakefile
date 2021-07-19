require 'fileutils'
require 'html-proofer'
require 'rspec/core/rake_task'

SITE_DIR           = './_site'
SITE_ID           = ENV['SITE_ID'] || 'api'

# configure default task
task default: :ci

desc 'Run the site locally on localhost:4000'
task :dev do
  sh 'bundle exec jekyll clean'
  sh 'bundle exec jekyll serve --watch --drafts'
end

desc 'Build CI site, run html-proofer and spec tests'
task :ci do
  Rake::Task['build:ci'].invoke
  Rake::Task['test:all'].invoke
end

namespace :build do
  def build(dest=nil, baseurl=nil)
    sh "bundle exec jekyll clean"
    cmd = "bundle exec jekyll build"
    cmd += " -d '#{dest}'" unless dest.nil?
    cmd += " --baseurl '#{baseurl}'" unless baseurl.nil?
    sh cmd
  end

  desc 'Clean and build with branch preview URL overrides'
  task :preview do
    branch = `git rev-parse --abbrev-ref HEAD`.strip
    baseurl = "/#{SITE_ID}/#{branch}"
    dest    = SITE_DIR + baseurl

    build dest=dest, baseurl=baseurl
  end

  desc 'Clean and build with CI test overrides'
  task :ci do
    baseurl = '/test/extra-test'
    dest    = SITE_DIR + baseurl

    build dest=dest, baseurl=baseurl
  end
end

namespace :test do
  RSpec::Core::RakeTask.new :spec

  task :all do
    Rake::Task['test:html'].invoke
    Rake::Task['test:links'].invoke
    Rake::Task['test:spec'].invoke
  end

  desc 'Check html'
  task :html do
    opts = {
      check_html: true,
      assume_extension: true,
      validation: {
        report_mismatched_tags: true,
        report_invalid_tags: true
      },
      disable_external: true,
      checks_to_ignore: ['LinkCheck']
    }
    HTMLProofer.check_directory(SITE_DIR, opts).run
  end

  desc 'Check for internal + *iiif.io* link errors'
  task :links do
    opts = {
      checks_to_ignore: ['ImageCheck', 'HtmlCheck', 'ScriptCheck'],
      url_ignore: [/^((?!iiif.io).)*$/, 'github']
    }
    HTMLProofer.check_directory(SITE_DIR, opts).run
  end

  desc 'Check for external link rot'
  task :linkrot do
    opts = {
      external_only: true,
      enforce_https: true,
      checks_to_ignore: ['ImageCheck', 'HtmlCheck', 'ScriptCheck']
    }
    HTMLProofer.check_directory(SITE_DIR, opts).run
  end
end

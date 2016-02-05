require 'html/proofer'
require 'rspec/core/rake_task'

RSpec::Core::RakeTask.new(:spec)

task :test do
  sh "bundle exec jekyll build" unless Dir.exists?('./_site')
  Rake::Task['spec'].invoke
  HTML::Proofer.new('./_site', cache: { timeframe: '2w' } ).run
end

task default: :test

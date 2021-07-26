spec = Gem::Specification.find_by_name 'iiifc-theme'
Dir.glob("#{spec.gem_dir}/lib/tasks/*.rake").each { |r| load r }

# configure default task
task ci: 'api:ci'
task default: :ci

namespace :api do
  desc 'run spec tests'
  task :spec do
    if File.file? './.rspec'
      `bundle exec rspec`
    else
      puts "Skipping rspec tests (no `./.rspec` file found)"
    end
    `sh scripts/check_json.py -v`
  end

  desc 'Run the site locally on localhost:4000'
  task :dev do
    sh 'bundle exec jekyll clean'
    sh 'bundle exec jekyll serve --watch --drafts'
  end

  desc 'Build CI site, run html-proofer and spec tests'
  task :ci do
    Rake::Task['build:ci'].invoke
    Rake::Task['test:html'].invoke
    Rake::Task['test:links:internal'].invoke
    Rake::Task['test:links:iiif'].invoke
    Rake::Task['api:spec'].invoke
  end
end

# config valid only for current version of Capistrano
lock '3.4.0'

set :log_level, :info

set :application, 'iiif.io'
set :repo_url, 'https://github.com/IIIF/iiif.io.git'

# Call with cap -s branch="<branchname>" deploy
ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }
set :env, "production"
set :deploy_to, '/home/iiif/repos/iiif.io'
set :build_to, '/home/iiif/Web/branches'

set :format, :pretty
set :linked_dirs, %w{api/image/validator api/presentation/validator}

set :keep_releases, 3

namespace :deploy do
  task :update_jekyll do
    on roles(:app) do
      within release_path do
        execute :bundle, "exec jekyll build -d #{fetch(:build_to)}/#{fetch(:branch)}"
      end
    end
  end
end

namespace :notify do
  desc 'Notify Google about sitemap update'
  task :google do
    run_locally do
      res = Net::HTTP.get(URI("http://www.google.com/ping?sitemap=http://#{application}/sitemap.xml"))
    end
  end
end

after "deploy:symlink:release", "deploy:update_jekyll"
after "deploy:published", "notify:google" if fetch(:branch) == 'master'

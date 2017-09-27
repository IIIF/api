require 'spec_helper'
require 'kramdown/document'

describe 'Editors' do

  they 'tend to screw up markdown' do

    report = {}
    glob_pattern = File.join(File.expand_path('../../../source', __FILE__), '**/*.md')
    markdown_files = Dir.glob(glob_pattern)
    links_include_path = File.expand_path('../../../source/_includes/links.md', __FILE__)
    links_include = File.open(links_include_path, 'rb').read
    markdown_files.each do |mf|
      unless %w{acronyms.md links.md}.any? { |inclood| mf.end_with? inclood }
        File.open(mf) do |f|
          src = f.read
          if src.include? "{% include links.md %}"
            src = [src, links_include].join('').gsub(/{% include links.md %}/, '')
          end
          errors = Kramdown::Document.new(src).warnings.grep(/link ID '[a-zA-Z][_0-9a-zA-Z-]*'/)
          unless errors.length == 0
            report[mf] = errors
          end
        end
      end
    end

    if report != {}
      $stderr.puts '*'*80
      report.each do |k,v|
        $stderr.puts k
        $stderr.puts v
      end
      $stderr.puts '*'*80
    end

    expect(report.empty?).to be_truthy

  end
end

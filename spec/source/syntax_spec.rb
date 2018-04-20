require 'spec_helper'
require 'kramdown/document'

DO_NOT_CHECK = %w{acronyms.md links.md}

def check_doc(src_str)
  # returns a hash of errors we care about
  if has_links_include?(src_str)
    src_str = add_links(src_str)
  end
  r = /link ID '[a-zA-Z][_0-9a-zA-Z-]*'/
  Kramdown::Document.new(src_str).warnings.grep(r)
end

def has_links_include?(src_str)
  src_str.include? "{% include links.md %}"
end

def links_include
  @links_include_path ||= File.expand_path('../../../source/_includes/links.md', __FILE__)
  @links_include ||= File.open(@links_include_path, 'rb').read
end

def add_links(src_str)
  [src_str, links_include].join('').gsub(/{% include links.md %}/, '')
end

def markdown_files
  glob_pattern = File.join(File.expand_path('../../../source', __FILE__), '**/*.md')
  Dir.glob(glob_pattern).reject do |path|
    DO_NOT_CHECK.any?{ |name| path.end_with? name }
  end
end

describe 'Editors' do

  they 'tend to screw up markdown' do
    report = {}
    markdown_files.each do |mf|
      File.open(mf) do |f|
        src = f.read
        errors = check_doc(src)
        unless errors.length == 0
          report[mf] = errors
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

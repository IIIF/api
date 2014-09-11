require 'spec_helper'
require 'kramdown/document'

describe 'Editors' do 

  they 'tend to screw up markdown' do
    
    report = {}
    # template = 'cat %s | kramdown 2>&1 >/dev/null | grep "link ID \'[a-zA-Z][_0-9a-zA-Z-]*\'"'
    glob_pattern = File.join(File.expand_path('../../../source', __FILE__), '**/*.md')
    markdown_files = Dir.glob(glob_pattern)
    markdown_files.each do |mf|
      unless mf.end_with?('acronyms.md')
        File.open(mf) do |f|
          errors = Kramdown::Document.new(f.read).warnings.grep(/link ID '[a-zA-Z][_0-9a-zA-Z-]*'/)
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

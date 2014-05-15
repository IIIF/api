require 'spec_helper'
require 'kramdown'
require 'json/ld'
require 'rdf/turtle'

IMAGE_API_MAJOR_VERSION = '2'
PRESENTATION_API_MAJOR_VERSION = '2'
JEKYLL_SERVER = 'localhost:4000'

describe 'The iiif.io site' do
  before(:all) do
    # Spin up Jekyll's server
    project_base = File.expand_path('../..', __FILE__)
    @server_pid = fork { exec "jekyll serve -s #{project_base} -d /tmp"  }
    sleep(5)
  end
  after(:all) do
    # Stop Jekyll's server
    Process.kill(9, @server_pid)
    Process.wait
  end

  describe 'Testing' do
    it 'works' do
      expect(true).to be_true
    end
    it "has access to the helper methods defined in the module" do
      expect(help).to be(:available)
    end
  end

  describe 'Each context and profile' do
    # Should also be well-formed JSON, at least. See what json/ld can do for us
  end

  describe 'Each JSON-LD codeblock in each file' do

    Dir['**/*.md'].select { |p| !p.include? 'README.md' }.each do |fp|

      doc = Kramdown::Document.new(File.read(fp), parse_block_html: true)
      cblk_list = descendants_from_element(doc.root) 

      it "should be parsable as JSON-LD (#{fp})" do
        cblk_list.each do |e|
          js = elem_value_without_syntax(e, 'javascript')
          json_str = strip_slash_comments_from_js(js)

          # Should be OK right from the doc
          expect { JSON.parse(json_str) }.not_to raise_error

          # Now replace iiif.io in URIS with localhost
          json_str.gsub!(/http:\/\/iiif\.io/, 'http://'+JEKYLL_SERVER)

          # Fake Jekyll expansion
          json_str.gsub!(/\{\{ site\.image_api\.latest\.major \}\}/, IMAGE_API_MAJOR_VERSION)
          json_str.gsub!(/\{\{ site\.presentation_api\.latest\.major \}\}/, PRESENTATION_API_MAJOR_VERSION)

          # Parse as JSON
          parsed_json = JSON.parse(json_str)
          # Do some stuff with it as JSON-LD
          expect { JSON::LD::API.expand(parsed_json) }.not_to raise_error
          
          graph = RDF::Graph.new
          expect { graph << JSON::LD::API.toRdf(parsed_json) }.not_to raise_error
          # puts graph.dump(:ttl) # this is fun!
        end
      end

    end

  end

end


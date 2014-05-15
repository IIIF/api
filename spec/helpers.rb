module Helpers

  # elem = Kramdown::Element
  def descendants_from_element(elem, code_syntax='javascript', cblk_list=[])
    elem.children.each do |e|
      cblk_list << e if (e.type == :codespan && e.value.start_with?(code_syntax))
      descendants_from_element(e, code_syntax, cblk_list) unless e.children.length == 0
    end
    cblk_list
  end

  def elem_value_without_syntax(element, code_syntax)
    element.value.split(code_syntax+"\n")[1]
  end

  def strip_slash_comments_from_js(js)
    # lines that are comments only [^  // my comment  $]
    wo_cmts = js.each_line.select { |l| !l.match /^\s*\/\// }
    # lines that are code and comments [^ "foo" : "bar" // my comment $]
    wo_cmts.each_with_index { |l, i| wo_cmts[i] = l.split(/[^:]\/\//)[0] } # keep '//' in URIs
    wo_cmts.join('')
  end

  # replace any jekyll interpolations with 'foo', just to get clean URIs
  # def foo_jekyll(json)
  #   json.each_with_index { |l, i| json[i] = l.gsub(/\{\{.+\}\}/, 'foo') }
  #   json
  # end

  def help
    :available
  end
end

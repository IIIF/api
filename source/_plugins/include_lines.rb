require 'liquid'

module Jekyll
  class IncludeLinesTag < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      super
      @markup = markup.to_s.strip
    end

    def render(context)
      site = context.registers[:site]
      source = site.source

      rendered_markup = Liquid::Template.parse(@markup).render(context)
      path, options = parse_markup(rendered_markup)
      raise ArgumentError, "include_lines: missing file path" if path.nil? || path.empty?

      from = integer_option(options, 'from')
      to = integer_option(options, 'to')
      start = integer_option(options, 'start')
      finish = integer_option(options, 'end')

      from ||= start
      to ||= finish

      format = true
      if options.key?('format')
        format = boolean_option(options, 'format')
      end
      indent = integer_option(options, 'indent')

      no_range_given = from.nil? && to.nil?

      # If no from/to (or start/end aliases) are given, include the whole file.
      # If only one of from/to is given, keep raising (ambiguous).
      if !no_range_given && !(from && to)
        raise ArgumentError, "include_lines: must specify from/to (1-indexed), e.g. {% include_lines path from:11 to:35 %}"
      end

      absolute_path = File.expand_path(path, source)
      unless absolute_path.start_with?(File.expand_path(source) + File::SEPARATOR)
        raise ArgumentError, "include_lines: path must be within the site source directory"
      end

      unless File.file?(absolute_path)
        raise ArgumentError, "include_lines: file not found: #{path}"
      end

      lines = File.read(absolute_path, encoding: 'UTF-8').split("\n", -1)
      max_line = lines.length

      if no_range_given
        from = 1
        to = max_line
      end

      if from < 1 || to < 1
        raise ArgumentError, "include_lines: from/to must be >= 1 (got from:#{from} to:#{to})"
      end

      if to < from
        raise ArgumentError, "include_lines: to must be >= from (got from:#{from} to:#{to})"
      end

      if from > max_line
        raise ArgumentError, "include_lines: from (#{from}) is beyond end of file (#{max_line} lines): #{path}"
      end

      to = [to, max_line].min

      selected = lines[(from - 1)..(to - 1)]

      if format
        selected = dedent_lines(selected)
      end

      if indent && indent > 0
        prefix = ' ' * indent
        selected = selected.map { |l| l.strip.empty? ? l : (prefix + l) }
      end

      selected.join("\n")
    rescue StandardError => e
      if defined?(Jekyll) && Jekyll.respond_to?(:logger) && Jekyll.logger
        Jekyll.logger.error("include_lines:", e.message)
      end
      raise
    end

    private

    def parse_markup(markup)
      tokens = markup.scan(/\"[^\"]+\"|\'[^\']+\'|\S+/)
      return [nil, {}] if tokens.empty?

      path_token = tokens.shift
      path = unquote(path_token)

      options = {}
      tokens.each do |t|
        key, value = t.split(':', 2)
        next if value.nil?
        options[key] = unquote(value)
      end

      [path, options]
    end

    def unquote(value)
      v = value.to_s
      if (v.start_with?('"') && v.end_with?('"')) || (v.start_with?("'") && v.end_with?("'"))
        v[1..-2]
      else
        v
      end
    end

    def integer_option(options, key)
      return nil unless options.key?(key)

      raw = options[key]
      return nil if raw.nil?

      s = raw.to_s.strip
      return nil if s.empty?

      Integer(s, 10)
    rescue ArgumentError
      raise ArgumentError, "include_lines: #{key} must be an integer (got #{raw.inspect})"
    end

    def boolean_option(options, key)
      return nil unless options.key?(key)

      v = options[key].to_s.strip.downcase
      return true if %w[1 true yes y on].include?(v)
      return false if %w[0 false no n off].include?(v)

      raise ArgumentError, "include_lines: #{key} must be a boolean (got #{options[key].inspect})"
    end

    def dedent_lines(lines)
      non_empty = lines.reject { |l| l.strip.empty? }
      return lines if non_empty.empty?

      min_indent = non_empty.map { |l| l[/\A[ \t]*/].length }.min
      return lines if min_indent.nil? || min_indent.zero?

      lines.map do |l|
        l.strip.empty? ? l : l[min_indent..]
      end
    end
  end
end

Liquid::Template.register_tag('include_lines', Jekyll::IncludeLinesTag)

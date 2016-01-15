# call_calendar_generator.rb
#
# To use:
# $ gem install ri_cal ice_cube tzinfo
# $ ruby call_calendar_generator.rb
#
# A new file, moderator_cal.ics will appear in the same directory

require "ice_cube"
require "ri_cal"
require "tzinfo"
require "date"

MODERATORS = [ "Appleby", "Crane", "Sanderson", "Stroop", "Warner" ]

# Make sure this is the date of a call or risk being off by a week.
PERIOD_START = Date.new(2016,01,06)
PERIOD_END = Date.new(2016,03,31)

def next_moderator
  next_mod = MODERATORS.shift
  MODERATORS.push(next_mod)
  next_mod
end

occurrences = IceCube::Schedule.new(start=PERIOD_START) { |s|
  s.add_recurrence_rule IceCube::Rule.weekly(2).day(:wednesday).until(PERIOD_END)
}.all_occurrences

dates = occurrences.map { |o| Date.parse(o.to_time.to_s) }

calendar = RiCal.Calendar do |cal|
  dates.each do |date|
    m = next_moderator
    label = "IIIF Bi-Weekly Community Call (#{m} moderates)"

    puts "#{date}: #{m}"

    dt_start = DateTime.parse("#{date.to_s}T12:00:00").set_tzid("America/New_York")
    dt_end = DateTime.parse("#{date.to_s}T01:00:00").set_tzid("America/New_York")

    cal.event do |event|
      event.summary = label
      event.description = label
      event.dtstart = dt_start
      event.dtend = dt_end
    end
  end
end

File.open('moderator_cal.ics', 'w') { |f| f.write(calendar) }

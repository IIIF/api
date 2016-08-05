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

MODERATORS = [ "Albritton", "Appleby", "Cramer", "Crane", "McGrattan",
  "Sanderson", "Snydman", "Rabun", "Stroop", "Warner" ].uniq.sort!

# Make sure this is the date of a call or risk being off by a week.
PERIOD_START = Date.new(2016,8,31)
PERIOD_END = Date.new(2017,1,14)

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
    labl = "IIIF Bi-Weekly Community Call (#{m} moderates)"
    description = "Moderator Link: https://stanford.bluejeans.com/639555055/1114/"

    puts "#{date}: #{m}"

    dt_start = DateTime.parse("#{date.to_s}T12:00:00").set_tzid("America/New_York")
    dt_end = DateTime.parse("#{date.to_s}T01:00:00").set_tzid("America/New_York")

    cal.event do |event|
      event.summary = labl
      event.description = description
      event.dtstart = dt_start
      event.dtend = dt_end
    end
  end
end

File.open('moderator_cal.ics', 'w') { |f| f.write(calendar) }

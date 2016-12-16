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

MODERATORS = {
    technical: [
      "Appleby",
      "Crane",
      "Sanderson",
      "Stroop",
      "Warner"
    ].uniq.sort!,
    community: [
      "Albritton",
      "Cramer",
      "McGrattan",
      "Snydman",
      "Rabun"
    ].uniq.sort!
}

# Make sure this is the date of a call or risk being off by a week.
PERIOD_START = Date.new(2017,01,18)
PERIOD_END = Date.new(2017,06,30)

class TopicTracker
  def initialize
    @next = :technical # this will be first
    @now = :community
  end

  def next
    @next, @now = @now, @next
    return @now
  end
end

def next_moderator(topic)
  next_mod = MODERATORS[topic].shift
  MODERATORS[topic].push(next_mod)
  next_mod
end

occurrences = IceCube::Schedule.new(start=PERIOD_START) { |s|
  s.add_recurrence_rule IceCube::Rule.weekly(2).day(:wednesday).until(PERIOD_END)
}.all_occurrences

dates = occurrences.map { |o| Date.parse(o.to_time.to_s) }

topic_tracker = TopicTracker.new

calendar = RiCal.Calendar do |cal|
  dates.each do |date|
    topic = topic_tracker.next
    m = next_moderator(topic)
    labl = "IIIF Bi-Weekly Community Call (#{topic.to_s}; #{m} moderates)"
    description = "Moderator Link: https://bluejeans.com/273449388/1114/"

    puts "#{date}: #{m} (#{topic.to_s})"

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

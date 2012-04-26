#!/usr/bin/env ruby -rubygems
############################################################
# throttle the notifications we send
# get 3 arguments
# "EMAIL" "SUBJECT" "BODY"
############################################################

unless ARGV.length == 3
  puts "usage: <> email subject body"
  exit
end

minimum_wait_time = 90   #seconds before we can alert again
alternative_email = "secondary-email@yourdomain.com" #send throttled alerts here when silenced

emailto = ARGV[0]
subject = ARGV[1]
details = ARGV[2]

email_p = emailto.gsub("@", "_").gsub(".", "_")


control_file = "/tmp/throttle_nagios_#{email_p}.txt"
mailer_cmd = "/usr/bin/mail"

if File.exists?(control_file)
  file_age = File.mtime(control_file)
  value = Time.now - file_age
  file_age_nice = sprintf("%1.1f", value)

  unless file_age_nice.to_f > minimum_wait_time.to_f
    system "/usr/bin/printf '%b' '#{details} (throttled due to a #{control_file} #{file_age_nice}s old' | #{mailer_cmd} -s '#{subject}' #{alternative_email}"
    Process.exit
  end
  
end

system "touch #{control_file}"
system "/usr/bin/printf '%b' '#{details}' | #{mailer_cmd} -s '#{subject}' #{emailto}"

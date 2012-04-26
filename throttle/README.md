## Email Throttling

The purpose is to prevent getting excessive emails from nagios on failed service/host events.

### Usage

#### Use as a notification

Multiple parameters can be used to suppress or throttle messages.

    usage: email_throttle [-h] [-i INITIAL] [-c COUNT] [-w WAIT] [-H HASH]
                          [-g GLOB] [--ignore_email] [-m MESSAGE] [-s SUBJECT]
                          [-e EMAIL] [-f FROM_EMAIL] [-d DATE]
                          [--message_format MESSAGE_FORMAT] [--temp TEMP]
                          [--database DATABASE] [--force] [--send] [--log LOG]
                          [--level LEVEL] [--job] [--skip_original_email]

    optional arguments:
      -h, --help            show this help message and exit
      -i INITIAL, --initial INITIAL
                            Number of seconds to wait before throttling
      -c COUNT, --count COUNT
                            Number of emails to send before throttling, supersedes
                            initial wait
      -w WAIT, --wait WAIT  Number of seconds to wait between bulk messages
      -H HASH, --hash HASH  Hash identifier, supersedes glob
      -g GLOB, --glob GLOB  Glob identifier, will be hashed for use
      --ignore_email        Do not include the email address in the hash
      -m MESSAGE, --message MESSAGE
                            Message
      -s SUBJECT, --subject SUBJECT
                            Subject
      -e EMAIL, --email EMAIL
                            To Email address
      -f FROM_EMAIL, --from_email FROM_EMAIL
                            From Email Address
      -d DATE, --date DATE  Date of the event
      --message_format MESSAGE_FORMAT
                            Format to use for storing messages (subject, then
                            message)
      --temp TEMP           Temp directory to store information
      --database DATABASE   Database file name
      --force               Always throttle
      --send                Always send
      --log LOG             Log file to write to
      --level LEVEL         Logging level
      --job                 Run in cron job cleanup mode
      --skip_original_email
                            When running in clean up mode, do not send to the
                            original sender  

#### Usage Examples

Test example

    /usr/bin/printf "%b" "### Nagios\n\nNotification Type: **PROBLEM**  \n\nService: site - example.com  \nHost: web-host-1a  \nAddress: example.com  \nState: **CRITICAL**  \n\nDate/Time: **Wed Apr 25 12:15:06 UTC 2012**  \n\nAdditional Info:\n\n**HTTP CRITICAL: HTTP/1.1 503 Service Temporarily Unavailable - string not found - 579 bytes in 0.442 second response time**  \n" | ./email_throttle -s "[PROBLEM] Service Alert: web-host-1a/example.com is CRITICAL" -e "who@example.com" -f "nagios@example.com"    

Working example

    /usr/bin/printf "%b" "### Nagios\n\nNotification Type: **$NOTIFICATIONTYPE$**  \n\nService: $SERVICEDESC$  \nHost: $HOSTALIAS$  \nAddress: $HOSTADDRESS$  \nState: **$SERVICESTATE**  \n\nDate/Time: **$LONGDATETIME$**  \n\nAdditional Info:\n\n**$SERVICEOUTPUT$**  \n" | email_throttle -s "[$NOTIFICATIONTYPE$] $SERVICESTATE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$" -e "$CONTACTEMAIL$" -f "nagios@example.com"

#### Cron Job Mode

In order to ensure that once a time window has been passed without having to wait for a new notification it should also be run as a cron job. In this mode it will check all hashes and send any that are past the wait window, and cleanup the records for each hash.

    email_throttle --job -f "nagios@example.com" -w 930 -s "[BULK NOTIFICATIONS] Service Alert(s)"

### What it's replacing

The standard nagios alert scripts are incapable of throttling, which can lead to a high volume of messages.

    /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$

    #$USER1$/send_mail.pl -n "SERVICE $NOTIFICATIONTYPE$" -h "$HOSTNAME$" -s "$SERVICESTATE$" -a "$HOSTADDRESS$" -i "$SERVICEDESC$ - $SERVICEOUTPUT$ - $SERVICECHECKCOMMAND$" -d "$LONGDATETIME$" -e "$CONTACTEMAIL$"

Testing Examples

    /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\nGroups: $SERVICEGROUPNAMES$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$

### Future features

In order to support future modifications an extra abstraction layer should be added for how to perform notifications. Ideally this will be either the next script to call, or a pluggable interface for each type of notification, whether it is email, SMS, AWS SNS, etc. 

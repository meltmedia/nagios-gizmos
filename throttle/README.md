## Email Throttling

The purpose is to prevent getting excessive emails from nagios on failed service/host events.

### Usage

#### Use as a notification

Multiple parameters can be used to suppress or throttle messages.

    -i, --initial COUNT
        Number of emails to send before throttling

    -w, --wait SECONDS
        Number of seconds to wait between bulk sends when messages are being throttled

    -h, --hash IDENTIFIER
        What to use as the glob identifier

    -m, --message, STDIN
        What to use as the body of the email

    -s, --subject SUBJECT
        What to use as the subject of the email

    -e, --email ADDRESS
        The email address to send to

    -d, --date
        The date of the event

Example

    email_throttle -i 3 -w 900 -h "$SERVICEGROUPNAMES$" -d "$LONGDATETIME$" -e "$CONTACTEMAIL$" -s "[$NOTIFICATIONTYPE$] Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$"

    email_throttle -i 3 -w 900 -h "GRAPES" -d "Tue Apr 24 13:43:59 MST 2012" -e "support-d@meltmedia.com" -s "[PROBLEM] Service Alert: Bob Dole/Generic Service is CRITICAL"

#### Cron Job Mode

In order to ensure that once a time window has been passed without having to wait for a new notification it should also be run as a cron job. In this mode it will check all hash and send if any are past the wait window, and cleanup the records for each hash.

### What it's replacing

The standard nagios alert scripts are incapable of throttling, which can lead to a high volume of messages.

    /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$

    #$USER1$/send_mail.pl -n "SERVICE $NOTIFICATIONTYPE$" -h "$HOSTNAME$" -s "$SERVICESTATE$" -a "$HOSTADDRESS$" -i "$SERVICEDESC$ - $SERVICEOUTPUT$ - $SERVICECHECKCOMMAND$" -d "$LONGDATETIME$" -e "$CONTACTEMAIL$"

Testing Examples

    /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\nGroups: $SERVICEGROUPNAMES$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$

### Future features

In order to support future modifications an extra abstraction layer should be added for how to perform notifications. Ideally this will be either the next script to call, or a pluggable interface for each type of notification, whether it is email, SMS, AWS SNS, etc. 

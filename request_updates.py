#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText

# For now, we'll just hardcode the sender and list of recipients
from_addy = 'Cyriac Kandoth <kandoth@cbio.mskcc.org>'
member_list = '/home/kandoth/src/weekly-update/subscribers.txt'
to_addys = {}
with open( member_list ) as fh:
    to_addys = dict( x.rstrip("\n>").split( " <", 1 ) for x in fh )

# Create the body of the plain-text message to request updates from people
email_body = """
Hope your week was good. Would you like to share with other CompOnc folks, what you've been up to,
and the issues you're troubleshooting? So I can automatically parse your reply, use the following
format to list as many items as you want to share with your colleagues:

- An article, link, or a new tool worth sharing
- A completed task, that you're super proud of, or glad to be done with
+ A task or topic you'll be working on next week
* An issue you're troubleshooting and could use help with

A script monitoring my inbox will parse your list, merge it with others, and on Saturday night,
everyone will get one consolidated email with everyone's lists. No worries if you don't want to
share anything this week. Wait another week or two if you feel you'll have more to report. Send me
a list anytime with "Weekly CompOnc Update" in the Subject, to save it for the next weekly email.

~Cyriac
"""

for name, to_addy in to_addys.iteritems():
    # Pull out the first name so we can say hi
    first_name = name.split()[0]
    text = "Hi " + first_name + ",\n" + email_body;

    # Create message container with MIME type text/plain
    msg = MIMEText( text, 'plain' )
    msg['Subject'] = "Weekly CompOnc Update"
    msg['From'] = from_addy
    msg['To'] = name + "<" + to_addy + ">"

    # Send the message via the local SMTP server
    smtp_svc = smtplib.SMTP( 'localhost' )
    smtp_svc.sendmail( from_addy, to_addy, msg.as_string())
    smtp_svc.quit()

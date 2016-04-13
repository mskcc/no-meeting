#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import expanduser
from datetime import date
from cgi import escape

# For now, we'll just hardcode the sender and list of recipients
from_addy = 'Cyriac Kandoth <kandoth@cbio.mskcc.org>'
member_list = '/home/kandoth/src/weekly-update/subscribers.txt'
to_addys = {}
with open( member_list ) as fh:
    to_addys = dict( x.rstrip("\n>").split( " <", 1 ) for x in fh )

# Find the latest file named after the current week in the year
iso_today = date.today().isocalendar()
[ iso_week, iso_year ] = [ str( iso_today[1] ), str( iso_today[0] )]
file_name = expanduser( "~" ) + '_'.join( [ '/Maildir/updates/week', iso_week, iso_year ]) + '.txt'

# Create the body of the message (a plain-text and an HTML version)
text = ""
with open( file_name ) as fh:
    text = text + fh.read()
html = "<html>\n<head></head>\n<body>\n" + escape( text, True ).replace( '\n', '<br />' ) + "\n</body>\n</html>"

# Record the MIME types of both parts - text/plain and text/html
part1 = MIMEText( text, 'plain' )
part2 = MIMEText( html, 'html' )

# Create message container with MIME type multipart/alternative
msg = MIMEMultipart( 'alternative' )
msg['Subject'] = "CompOnc updates from last week"
msg['From'] = from_addy

# Attach parts into message container. According to RFC 2046, the last part of a multipart message,
# in this case the HTML message, is best and preferred
msg.attach( part1 )
msg.attach( part2 )

for name, to_addy in to_addys.iteritems():
    # Send the message via the local SMTP server
    msg['To'] = name + "<" + to_addy + ">"
    smtp_svc = smtplib.SMTP( 'localhost' )
    smtp_svc.sendmail( from_addy, to_addy, msg.as_string())
    smtp_svc.quit()

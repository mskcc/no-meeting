#!/usr/bin/env python

import smtplib, re

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import expanduser, isfile
from datetime import date
from cgi import escape

# For now, we'll just hardcode the sender and list of recipients
from_addy = 'Cyriac Kandoth <kandoth@cbio.mskcc.org>'
home_dir = expanduser( "~" )
member_list = home_dir + '/src/weekly-update/subscribers.txt'
to_addys = {}
with open( member_list ) as fh:
    to_addys = dict( x.rstrip("\n>").split( " <", 1 ) for x in fh )

# Find the latest file named after the current week in the year
iso_today = date.today().isocalendar()
[ iso_week, iso_year ] = [ str( iso_today[1] ), str( iso_today[0] )]
file_name = home_dir + '_'.join( [ '/Maildir/updates/week', iso_week, iso_year ]) + '.txt'

# Quit with error if we can't find the file
if not isfile( file_name ):
    sys.exit( 1 )

# Load the file directly as a plain-text version of the email
email_plain = ""
with open( file_name ) as fh:
    email_plain = email_plain + fh.read()

# Create a template for the HTML version of the email
email_html = """
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>CompOnc updates from last week</title>
</head>
<body>
"""

# Convert the plain-text email to lists with colored bullets
for line in email_plain.splitlines():
    line = escape( line, True )
    m = re.match( '^(-|\+|\*)\s*(\S.*\S)\s*$', line )
    if m and m.group( 1 ) is '-':
        line = "<li class=\"done\" style=\"color:blue;list-style-type:disc;font-size:16px;\"><span style=\"color:black;font-size:13px;\">" + m.group( 2 ) + "</span></li>\n"
    elif m and m.group( 1 ) is '+':
        line = "<li class=\"todo\" style=\"color:blue;list-style-type:circle;font-size:16px;\"><span style=\"color:black;font-size:13px;\">" + m.group( 2 ) + "</span></li>\n"
    elif m and m.group( 1 ) is '*':
        line = "<li class=\"help\" style=\"color:red;list-style-type:disc;font-size:16px;\"><span style=\"color:black;font-size:13px;\">" + m.group( 2 ) + "</span></li>\n"
    else:
        line = "<span style=\"font-weight:bold;font-size:13px;\">" + line + "</span><br>"
    email_html += line

email_html += """
</body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html
part1 = MIMEText( email_plain, 'plain' )
part2 = MIMEText( email_html, 'html' )

for name, to_addy in to_addys.iteritems():
    # Create message container with MIME type multipart/alternative
    msg = MIMEMultipart( 'alternative' )
    msg['Subject'] = "CompOnc updates from last week"
    msg['From'] = from_addy
    msg['To'] = name + "<" + to_addy + ">"

    # Attach parts into message container. According to RFC 2046, the last part of a multipart message,
    # in this case the HTML message, is best and preferred
    msg.attach( part1 )
    msg.attach( part2 )

    # Send the message via the local SMTP server
    smtp_svc = smtplib.SMTP( 'localhost' )
    smtp_svc.sendmail( from_addy, to_addy, msg.as_string())
    smtp_svc.quit()

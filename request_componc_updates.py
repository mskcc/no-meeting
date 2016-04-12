#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

my_addy = "kandoth@cbio.mskcc.org"
your_addy = "harrisc2@mskcc.org"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart( 'alternative' )
msg['Subject'] = "Weekly CompOnc Update"
msg['From'] = my_addy
msg['To'] = your_addy

# Create the body of the message (a plain-text and an HTML version).
text = """
Hi buddy ol pal! Hope your week was good. Would you like to share with other CompOnc folks, what you've been up to?
So I can parse your reply properly, use the following format:
- Accomplishments\n+ Upcoming tasks\n* Bottlenecks
"""
html = """
<html>
    <head></head>
    <body>
    <p>Hi buddy ol pal! Hope your week was good. Would you like to share with other CompOnc folks, what you've been up to?</p>
    <p>So I can parse your reply properly, use the following format:</p>
    <p>
        - Accomplishments<br>
        + Upcoming tasks<br>
        * Bottlenecks<br>
    </p>
    </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText( text, 'plain' )
part2 = MIMEText( html, 'html' )

# Attach parts into message container. According to RFC 2046, the last part of a multipart message,
# in this case the HTML message, is best and preferred.
msg.attach( part1 )
msg.attach( part2 )

# Send the message via local SMTP server.
smtp_srv = smtplib.SMTP( 'localhost' )
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
smtp_srv.sendmail( my_addy, your_addy, msg.as_string())
smtp_srv.quit()

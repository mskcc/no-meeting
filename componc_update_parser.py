#!/usr/bin/env python

import sys,re,email

from datetime import date

mail = email.message_from_string( sys.stdin.read() )
sender = mail['from']
body = ""

# For multipart emails, we need to extract the plain-text part
if mail.is_multipart():
    for part in mail.walk():
        ctype = part.get_content_type()
        cdispo = str( part.get( 'Content-Disposition' ))

        # skip any text/plain (txt) attachments
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload( decode=True )
            break
# not multipart - i.e. plain text, no attachments
else:
    body = mail.get_payload( decode=True )

today = date.today()
iso_today = today.isocalendar()
week = '_'.join( [ 'componc_updates/week', str( iso_today[1] ), str( iso_today[0] ) ]) + '.txt'
fh = open( week, 'a' )
fh.write( "\n" + sender + ":\n" )
for line in body.splitlines():
    if re.match( '-|\+|\*', line ):
        fh.write( line + "\n" )

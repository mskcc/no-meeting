#!/usr/bin/env python

import sys, re, email

from os.path import expanduser
from datetime import date

mail = email.message_from_file( sys.stdin )
sender = mail['from']
body = ""

# For multipart emails, we need to extract the plain text part
if mail.is_multipart():
    for part in mail.walk():
        ctype = part.get_content_type()
        cdispo = str( part.get( 'Content-Disposition' ))

        # skip any text/plain (txt) attachments
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload( decode=True )
            break
# If it's not multipart, then it's just plain text, with no attachments
else:
    body = mail.get_payload( decode=True )

# Create/append a file named after the current week in the year
iso_today = date.today().isocalendar()
[ iso_week, iso_year ] = [ str( iso_today[1] ), str( iso_today[0] )]
file_name = expanduser( "~" ) + '_'.join( [ '/Maildir/updates/week', iso_week, iso_year ]) + '.txt'
fh = open( file_name, 'a' )
fh.write( "\n" + sender + ":\n" )
for line in body.splitlines():
    if re.match( '-|\+|\*', line ):
        # Use regexes to cleanup whitespace
        line = re.sub( '^(-|\+|\*)\s*(\S.*\S)\s*$', '\g<1> \g<2>', line )
        fh.write( line + "\n" )
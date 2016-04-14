#!/usr/bin/env python

import sys, re, email

from os.path import expanduser
from datetime import date

home_dir = expanduser( "~" )
mail = email.message_from_file( sys.stdin )
sender = mail['from']

# Do some cleanup on the sender's name and email
m = re.match( '^"?([^,]*),\s+([^\/]*)/.*"?\s+(<\S+>)$', sender )
if m:
    sender = ' '.join( m.group( 2, 1, 3 ))

# For multipart emails, we need to extract the plain text part
body = ""
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
file_name = home_dir + '_'.join( [ '/Maildir/updates/week', iso_week, iso_year ]) + '.txt'

fh = open( file_name, 'a' )
fh.write( sender + ":\n" )
for line in body.splitlines():
    if re.match( '-|\+|\*', line ):
        # Stop parsing the file if we reached the original message
        if re.match( '-----Original Message-----', line ):
            break
        # Cleanup whitespace
        line = re.sub( '^(-|\+|\*)\s*(\S.*\S)\s*$', '\g<1> \g<2>', line )
        # Remove embedded links
        line = re.sub( ' <http\S+>', '', line )
        fh.write( line + "\n" )
fh.write( "\n" )

## weekly-update

To install, put these scripts 
- `subscribers.txt` lists all the folks that will receive reminders to send updates
- `request_updates.py` sends email reminders to that list of folks updates
- `parse_update.py` parses emails piped into it by procmail, and appends them to a weekly text file
- `send_updates.py` sends the weekly text file to a mailing list or the same subscribers

The following files are set up at the `cbio.mskcc.org` SMTP server for user `kandoth`.

### ~/.forward
```
"|IFS=' ' && exec /usr/bin/procmail || exit 75 #kandoth"
```
Ensures that procmail is run for every email received

### ~/.procmailrc
```
# Make sure we're not using any C-based shells. Procmail does weird things on those
SHELL=/bin/sh

# Turn off comsat notifications in CLI, because they're annoying
COMSAT=no

# Set the default paths of where mail should go
DEFAULT=$HOME/Maildir/
MAILDIR=$HOME/Maildir/

# Keep a log file for debugging procmail
LOGFILE=$HOME/procmail.log
LOGABSTRACT=all
VERBOSE=off

# Send update emails into a subfolder, and pipe them into a script that parses & accumulates them
:0: fw
* ^Subject.*(Weekly CompOnc Update)
{
    :0 c
    updates/raw

    :0:
    | /usr/bin/env python $HOME/src/weekly-update/parse_update.py
}
```
Every email with the subject line `Weekly CompOnc Update` will be piped into `parse_update.py`.

### crontab -e
```
0 16 * * 5 /usr/bin/env python $HOME/src/weekly-update/request_updates.py
0 21 * * 6 /usr/bin/env python $HOME/src/weekly-update/send_updates.py
```
At 4p every Friday, remind folks to send updates. And 9p on Saturdays, send out accumulated updates

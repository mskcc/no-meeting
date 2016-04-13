## weekly-update
- `request_updates.py` sends emails to a list of folks requesting updates in the following format:
```
- Accomplishment
+ Upcoming task
* Bottleneck
```
- `parse_update.py` parses out updates from emails piped into it by procmail, and appends them to a weekly text file
- `send_updates.py` sends the weekly text file to a mailing list

The following files are set up at the `cbio.mskcc.org` mail server for user `kandoth`.

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
55 23 * * 6 /usr/bin/env python $HOME/src/weekly-update/send_updates.py
```
Runs `request_updates.py` every Friday at 4p to remind folks to send back updates

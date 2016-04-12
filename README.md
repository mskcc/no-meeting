## weekly-update
- `request_updates.py` sends weekly emails to a list of folks requesting updates in the following format:
```
- Accomplishments
+ Upcoming tasks
* Bottlenecks
```
- `update_parser.py` parses replies piped to it by procmail and writes updates in a weekly text file
- ::TODO:: `send_updates.py` sends the weekly text file to a mailing list

The following files are set up at the `cbio.mskcc.org` mail server for user `kandoth`.

### ~/.forward
```
"|IFS=' ' && exec /usr/bin/procmail || exit 75 #kandoth"
```
Ensures that procmail is run for every email received

### ~/.procmailrc
```
# Make sure we're not using any C-based shells. Procmail does wierd things on those
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

# Pipe CompOnc update emails to a script that parses and summarizes them for redistribution
:0: fw
* ^Subject.*(Weekly CompOnc Update)
| /usr/bin/env python $HOME/src/weekly-update/update_parser.py
```
Every email with the subject line `Weekly CompOnc Update` will be piped to the script, and the user won't see it in their inbox.

### crontab -e
```
0 17 * * 5 /usr/bin/env python $HOME/src/weekly-update/request_updates.py
```
Sends a request for updates every Friday at 5p

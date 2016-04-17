## no-meeting

To install, put these in your `$HOME/src/no-meeting`:
- `subscribers.txt` lists all the folks that will receive reminders to send updates
- `request_updates.py` sends email reminders to that list of folks, to reply in this format:
```text
- An article, link, or a new tool worth sharing
- A completed task, that you're super proud of, or glad to be done with
+ A task or idea you'll be working on this week
* An issue you're troubleshooting and could use help with
```
- `parse_update.py` parses emails piped into it, and stores them into weekly text files.
- `send_updates.py` reformats updates like below, and sends it around to the same folks.
![sampler](/sampler.png)

The following files are set up at the `cbio.mskcc.org` SMTP server. Just replace `kandoth` with your username.

### ~/.forward
```bash
"|IFS=' ' && exec /usr/bin/procmail || exit 75 #kandoth"
```
Ensures that procmail is run for every email received

### ~/.procmailrc
```bash
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
* ^Subject.*(Share updates and issues with colleagues)
{
    :0 c
    updates/raw

    :0:
    | /usr/bin/env python $HOME/src/no-meeting/parse_update.py
}
```
Every email with the subject line `Share updates and issues with colleagues` will be piped into `parse_update.py`, and a copy of the original will be kept under the IMAP folder updates/raw

### crontab -e
```
0 09 * * 1 /usr/bin/env python $HOME/src/no-meeting/request_updates.py
0 14 * * 2 /usr/bin/env python $HOME/src/no-meeting/send_updates.py
```
At 9a on Mondays, remind folks to send updates. At 2p on Tuesdays, send around accumulated updates

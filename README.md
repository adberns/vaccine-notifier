# VaccineSpotter.org Notifier
A hastily made Python script to get data from www.vaccinespotter.org and send email notifications when a new open vaccination slot appears.

To configure, copy `config.py.template` to `config.py` and specify:
* email address and password (I suggest using Google's App Password here)
* email addresses of those to notify
* state to search (two letter abbreviation)

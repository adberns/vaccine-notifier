#!/usr/bin/python3
import requests
import smtplib
import config
from email.message import EmailMessage


def get_openings():
  full_data = requests.get('https://www.vaccinespotter.org/api/v0/states/' + config.STATE_ABBR + '.json').json()['features']

  results = []

  for pharmacy_record in full_data:
    pharmacy = pharmacy_record['properties']
    if 'appointments_available' in pharmacy and pharmacy['appointments_available']:
      results.append(pharmacy)

  return results


def notify_for_new(pharmacy_info):
  try:
    with open('.vaccine_openings') as input_file:
      old_results = input_file.readlines()
      old_results = [location.strip() for location in old_results]
  except FileNotFoundError:
    old_results = []

  new_results = []
  notifications = ''

  for pharmacy in pharmacy_info:
    new_results.append(pharmacy['provider_location_id'])

    # Just getting the string representations of these because I don't
    # want to check for None types each time - might fix later
    if pharmacy['provider_location_id'] not in old_results:
      notifications += str(pharmacy['name']) + ', ' + str(pharmacy['address']) \
                       + ', ' + str(pharmacy['city']) \
                       + ' (' + str(pharmacy['provider_brand_name']) + ')\n'

  with open('.vaccine_openings', 'w') as output_file:
    output_file.write('\n'.join(new_results) + '\n')
  
  if len(notifications):
    for recipient in config.NOTIFY_LIST:
      notify(notifications, recipient)


# Taken from 
#   https://stackoverflow.com/questions/60975490/how-does-one-send-an-e-mail-from-python-not-using-gmail
def notify(message, destination):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(config.FROM_ADDRESS, config.FROM_PASSWORD)

  msg = EmailMessage()

  message = f'{message}\n'
  msg.set_content(message)
  msg['Subject'] = 'COVID-19 Vaccine Update'
  msg['From'] = config.FROM_ADDRESS
  msg['To'] = destination
  server.send_message(msg)


if __name__=='__main__':
  notify_for_new(get_openings())

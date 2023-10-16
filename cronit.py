#!/bin/python3

# required dependancies 'pip3 install pytz' if on python < 3.9
# AEST to UTC time conversion and cron schedule generator
# intended use is to alias the location of script to cronit eg alias cronit='~/$path to script/cronit.py'
# usage '$ cronit 3pm 15-10-23' will output UTC time for comfirmation and schedule depending on inputs
# do not forget to chmod +x the file

import re, sys, pytz
from datetime import datetime, timedelta

def format_time(time):
    # regex
    time_pattern = r'(\d+)(?::(\d+))?(\s*am|\s*pm)?'

    # get the current AEST time
    now = datetime.now(pytz.timezone('Australia/Brisbane'))

    # result time
    result_time = None

    # time pattern
    time_match = re.match(time_pattern, time, re.IGNORECASE)

    if time_match:
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2)) if time_match.group(2) else 0
        am_pm = time_match.group(3)

        # adjust hours based on am/pm
        if am_pm and am_pm.strip().lower() == 'pm' and hours != 12:
            hours += 12

        result_time = now.replace(hour=hours, minute=minutes)

    # check if the time is previous day
    if result_time < now:
        result_time += timedelta(days=1)

    # error handling
    if result_time is None:
        print('¯\_(ツ)_/¯ please enter a correct time format. e.g. 2pm dd-mm-yy or 2:00pm dd-mm-yyyy')
        return None

    return result_time

# check arguments are passed
if len(sys.argv) < 3:
    print("Enter AEST time & date to convert to UTC for a cron schedule.\nAccepted Formats: 12pm dd-mm-yyyy, 12:00 dd-mm-yy")
else:
    time = sys.argv[1]
    date = sys.argv[2]
    converted_time = format_time(time)

    # convert AEST to UTC and print for visual aid
    if converted_time:
        aest_time = converted_time.strftime('%H:%M %d-%m-%Y')
        utc_time = converted_time.astimezone(pytz.UTC).strftime('%H:%M %d-%m-%Y')
        print(f"\nAEST Time: {aest_time}\nUTC Time: {utc_time}\n")
        hour = converted_time.astimezone(pytz.UTC).strftime('%H')
        minute = converted_time.astimezone(pytz.UTC).strftime('%M')

        # grab inputs for cron jobs
        freq = input('Do you want this to be [d]aily, [w]eekly, or [m]onthly?  ').lower()
        while freq not in ['d', 'daily', 'w','weekly', 'm', 'monthly']:
            print('¯\_(ツ)_/¯ ruhroh please enter daily, weekly, or monthly.')
            freq = input('Do you want this to be [d]aily, [w]eekly, or [m]onthly? ').lower()

        # daily cron format
        if freq == "daily" or freq == 'd':
            print(f'''
 ┌───────────── minute (0 - 59)
 │  ┌───────────── hour (0 - 23)
 │  │  ┌───────────── day of the month (1 - 31 or * for every day)
 │  │  │ ┌───────────── month (1 - 12 or * for every month)
 │  │  │ │ ┌───────────── day of the week 0 - 6, Sunday to Saturday or * for every day
 {minute} {hour} * * *\n''')

        # weekly cron format
        elif freq == "weekly" or freq == 'w':
            days_of_week = {'sun': 0,'mon': 1,'tues': 2,'wed': 3,'thurs': 4,'fri': 5,'sat': 6}

            while True:
                day = input('What day? Sun, Mon, Tues, Wed, Thurs, Fri, Sat: ').lower()
                if day in days_of_week:
                    day = days_of_week[day]
                    break
                print('¯\_(ツ)_/¯ ruhroh please enter a valid day of the week.')

            print(f'''
 ┌───────────── minute (0 - 59)
 │  ┌───────────── hour (0 - 23)
 │  │  ┌───────────── day of the month (1 - 31 or * for every day)
 │  │  │ ┌───────────── month (1 - 12 or * for every month)
 │  │  │ │ ┌───────────── day of the week 0 - 6, Sunday to Saturday or * for every day
 {minute} {hour} * * {day}\n''')

        # monthly cron format
        elif freq == "monthly" or freq == 'm':
            while True:
                date = input('What day? Enter date between 1 and 31: ')
                if date.isdigit():
                    date = int(date)
                    if 1 <= date <= 31:
                        break
                print('¯\_(ツ)_/¯ ruhroh please enter date between 1 and 31.')

            print(f'''
 ┌───────────── minute (0 - 59)
 │  ┌───────────── hour (0 - 23)
 │  │  ┌───────────── day of the month (1 - 31 or * for every day)
 │  │  │  ┌───────────── month (1 - 12 or * for every month)
 │  │  │  │ ┌───────────── day of the week 0 - 6, Sunday to Saturday or * for every day
 {minute} {hour} {date} * *\n''')

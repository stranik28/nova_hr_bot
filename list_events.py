import datetime
from cal_setup import get_calendar_service

def main(hours):
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=-1*hours)
    end = now+ datetime.timedelta(hours = 12)
    # print(now)
    # print(end)
    end = end.isoformat() + 'Z' # 'Z' indicates UTC time
    # print(type(now))
    now = now.isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting List o 10 events')
    events_result = service.events().list(
        calendarId='rvvnp6be9ga1nc4ada51j7t2sc@group.calendar.google.com', timeMin=now,
        timeMax=end, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    #     # print(event)
    return events

if __name__ == '__main__':
   main()
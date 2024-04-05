import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import pytz
import subprocess
import time
class GoogleCalendar():
      def __init__(self, calId):
         self.service = self.getService()
         self.calId = calId
         self.tz = self.getTz()
         self.events = []
         self.preEvents = {}

      #sets up api access
      def getService(self):
         SCOPES = 'https://www.googleapis.com/auth/calendar' #'https://www.googleapis.com/auth/calendar'
         CLIENT_SECRET_FILE = 'client_secret_cal.json'
         APPLICATION_NAME = 'Life Management Google Calendar API'
         credentialDir = os.path.join(os.path.expanduser('~'), '.credentials')
         if not os.path.exists(credentialDir):
              os.makedirs(credentialDir)
         credential_path = os.path.join(credentialDir, 'calendar-python-life-manadgement.json')
         store = Storage(credential_path)
         credentials = store.get()
         if not credentials or credentials.invalid:
              flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
              flow.user_agent = APPLICATION_NAME
              credentials = tools.run_flow(flow, store)
              print('Storing credentials to ' + credential_path)
         return discovery.build('calendar', 'v3', http=credentials.authorize(httplib2.Http()))
      #gets the timezone
      def getTz(self):
          return self.getCalendar()["timeZone"]
      #get a google calendar 
      def getCalendar(self):
          return self.service.calendars().get(calendarId=self.calId).execute()
      #gets all events from today
      def getCurrEvents(self):
          return self.getOffsetEvents(0)
      #gets all events a sepecific number of days from now
      def getOffsetEvents(self, offset):
          now = (datetime.datetime.utcnow()).isoformat()+ 'Z'
          end = (datetime.datetime.utcnow()+datetime.timedelta(minutes=1, hours=offset)).isoformat()+'Z'
          ret = self.service.events().list(calendarId=self.calId, timeMin=now, timeMax=end, singleEvents=True).execute()['items']
          return [i for i in ret if i["id"] not in self.preEvents and "dateTime" in i["end"]]
      #creates and event at the date
      def addEvent(self, title, date, start_time, length, loc="", desc="", recur=False, untill=False):
          timezone = self.tz
          start = pytz.timezone(timezone).localize(datetime.datetime.combine(date, start_time))
          end = start + datetime.timedelta(minutes=length)
          event = {'summary': title,
               'start':  {'dateTime': start.isoformat(), 'timeZone': timezone},
               'end':    {'dateTime': end.isoformat(), 'timeZone': timezone},
               'description' : desc, 'location' : loc,
               'recurrence' : [self.rrule(recur, untill)]}
          e = self.service.events().insert(calendarId=self.calId, body=event).execute()           
      #formates a recuring rule such that google calendar can read it
      def rrule(self, recur, untill):
          if untill:
             end_date = str(untill.year)
             if untill.month < 10:
                end_date += '0' + str(untill.month)
             else:
                end_date += str(untill.month)
             if untill.day < 10:
                end_date += '0' + str(untill.day)
             else:
                end_date += str(untill.day)
             end = ';UNTIL={}'.format(end_date)
          else:
             end = ''
          if recur:
             return "RRULE:FREQ=WEEKLY" + end
          else:
             return None
      #cleans self
      def filterPreEvent(self):
          for i in list(self.preEvents.keys()):
              if self.preEvents[i]<time.time():
                 del self.preEvents[i]
      def getOffsetEvent(self, offset):
          if self.events == []:
             self.filterPreEvent()
             self.events = self.getOffsetEvents(offset)
             for i in self.events:
                 self.preEvents[i["id"]] = datetime.datetime.strptime(
                                ''.join(i["end"]["dateTime"].rsplit(':', 1)),
                                "%Y-%m-%dT%H:%M:%S%z").timestamp()
             return None
          else:
             ret = self.events[0]
             self.events = self.events[1:]
             return ret
      def getCurrEvent(self):
          return self.getOffsetEvent(0)

class GoogleCalendarGroup():
      def __init__(self, calIds = None):
          if not calIds:
             ret = []
             for i in GoogleCalendar.getService(None).calendarList().list().execute()["items"]:
                 ret.append(GoogleCalendar(i["id"]))
             self.cals = ret
          else:
             self.cals = [GoogleCalendar(i) for i in calIds]
      def getOffsetEvents(self, offset):
          ret = []
          for i in self.cals:
            ret = ret + i.getOffsetEvents(offset)
          return ret
      def getCurrEvents(self):
          return self.getOffsetEvents(0)
      def getOffsetEvent(self, offset):
          for i in self.cals:
            ret = i.getOffsetEvent(offset)
            if ret != None:
               return ret
          return None
      def getCurrEvent(self):
          return self.getOffsetEvent(0)


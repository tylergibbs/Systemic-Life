from machine import *
import typeforms
import googleSheets
import re
import datetime
import random
import googleCalendar
import sms
from splitWise import SplitWise
from splitwise.user import ExpenseUser
from splitwise.expense import Expense
def parseTime(time):
   offset = 12 if ('PM' in time) else 0
   split = time.find(':')
   hour = int(time[:split])+offset
   minu = int(time[split+1:split+3])
   return datetime.time(hour, minu)

class getTypeform(noIn):
      def __init__(self, api_key, key):
          self.typeform = typeforms.Typeform(api_key, [key])
          def f():
              ft = self.typeform.getTypeform()
              if not ft:
                 return None
              else:
                 return Item([],ft)
          super().__init__(f)

#############################
#######Typeform Efects#######
#############################
#when appified will be broken up and re thought
class AddHwSeries(noOut):
      def __init__(self):
          def doHwSeries(tf):
              rst = "(\d\d?/\d\d?/(?:\d\d)?\d\d)(?: ([^!]+?) |$)?(?: !)?"
              clas = tf['textfield_BnYpl9rTUP1g']
              dates = tf['textarea_n0vJQRyOpC1p']
              i = 1
              for (date, name) in re.findall(rst, dates):
                  print(date)
                  print(name)
                  if len(date) == 6:
                     date = date[:-2] + "20" + date[-2:]
                  date = re.findall('([0-9]+)[/-]([0-9]+)[/-]([0-9]+)', date)[0]
                  date = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
                  print(date)
                  time = datetime.datetime.strptime(random.choice(['9:00', '10:00', '11:00', '12:00', '13:00', '14:00',\
                                   '15:00', '16:00', '17:00', '18:00']), '%H:%M').time()
                  print(time)
                  if name:
                     name = clas + ' ' + name
                  else:
                     name = clas + ' ' + str(i)
                     i+=1
                  googleCalendar.GoogleCalendar('mjni7ep3fff5n451kn1e1atgfo@group.calendar.google.com')\
                           .addEvent(name, date, time, 60)
          super().__init__(doHwSeries)

class AddClass(noOut):
      def __init__(self):
          def addClass(tf, blockDate):
              print("addClass")
              rst = "([^ ][^ ][^ ])? (..?:..?(?: ..)?) (\d+)( [^ !]+)?(?: !)?"
              dayMap = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 'Thu':'Thursday',
                        'Fri':'Friday', 'Sat':'Saterday', 'Sun':'Sunday'}
              name  = tf['textfield_nLTVNT9wELfr']
              quart = tf['list_KxWegwY2QpyD_choice']
              dfuloc= tf['textfield_aDZDdkrnOTt3']
              placeTimes= tf['textfield_Nb0iuQCndnll']
              finalDate = ""
              finalTime = ""
              finalLoc = ""
              if 'date_GTrhwaWkcc9G' in tf.keys() and 'textfield_iV2DEae1jXgm' in tf.keys():
                 finalDate = tf['date_GTrhwaWkcc9G']
                 finalTime = tf['textfield_iV2DEae1jXgm']
                 if 'textfield_t6mI2MJMAiWa' in tf.keys():
                    finalLoc  = tf['textfield_t6mI2MJMAiWa']
              end_date = blockDate[quart]["endDate"]
              print(re.findall(rst, placeTimes)) 
              for (day, time, leng, loc) in re.findall(rst, placeTimes):
                  if not loc:
                     loc = dfuloc
                  date = blockDate[quart][dayMap[day]]
                  time = parseTime(time)
                  leng = int(leng)
                  print("event" + day)
                  googleCalendar.GoogleCalendar('1jl6euiiosnpuv684k2062jmng@group.calendar.google.com')\
                             .addEvent(name, date, time, leng, loc, '', True, end_date)
              if finalDate:
                 finalDate = re.findall('([0-9]+)[/-]([0-9]+)[/-]([0-9]+)', finalDate)[0]
                 print(finalDate)
                 finalDate = datetime.datetime(int(finalDate[0]), int(finalDate[1]), int(finalDate[2]))
                 googleCalendar.GoogleCalendar('1jl6euiiosnpuv684k2062jmng@group.calendar.google.com')\
                             .addEvent(name + "Final", finalDate, parseTime(finalTime), 180, finalLoc, '')
          super().__init__(addClass)
  

class AddSmallProj(noOut):
      def __init__(self):
         def doSmallProj(tf):
             due = tf['date_cz1IZyrLsumH'].replace("-", "/")
             start = str(datetime.datetime.now().date()).replace("-","/")
             if 'date_OjRb23VQQcaJ' in tf.keys():
                start=tf['date_OjRb23VQQcaJ'].replace("-", "/")
             name= tf['textfield_zzgAihi3dqd3']
 
             date = re.findall('([0-9]+)[/-]([0-9]+)[/-]([0-9]+)', due)[0]
             print(date)
             date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
             time = parseTime(random.choice(['9:00', '10:00', '11:00', '12:00', '13:00', '14:00',\
                                   '15:00', '16:00', '17:00', '18:00']))

             googleCalendar.GoogleCalendar('mjni7ep3fff5n451kn1e1atgfo@group.calendar.google.com')\
                           .addEvent(name, date, time, 60, desc = start)
         super().__init__(doSmallProj)

class AddRecuringQuarterEvent(noOut):
      def __init__(self):
         def doRecuringQuarterEvent(tf, blockDate):
            name = tf['textfield_mzujuUp3Ylvg']
            days = []
            for i in tf.keys():
                if 'list_sD2tpF68j1Dl_choice_' in i:
                    days = days + [tf[i]]
            desc = ""
            if 'textarea_oGuXn8SGZOLy' in tf.keys():
               desc = tf['textarea_oGuXn8SGZOLy']
            quart = tf['list_KpxwJHMv9NKp_choice']
            title = tf['textfield_mzujuUp3Ylvg']
            loc = ""
            if 'textfield_wXaMZXJtkOlK' in tf.keys():
               loc = tf['textfield_wXaMZXJtkOlK']
            time = parseTime(tf['textfield_oaxetgcsUzgN'])
            length = int(tf['number_znnSHyFhwyij'])

            startDates = [blockDate[quart][i] for i in days]
            endDate = blockDate[quart]["endDate"] 
            
            for date in startDates:
               googleCalendar.GoogleCalendar('1jl6euiiosnpuv684k2062jmng@group.calendar.google.com')\
                             .addEvent(name, date, time, length, loc, desc, True, endDate)
         super().__init__(doRecuringQuarterEvent)
#Xfywnm
#{'textfield_Maf3TeF00J84': 'test', 'list_SFFmFqOvH1Xv_choice_I4zHIMt0AQYw': 'Rivka', 'list_uDy8LvuB3wTa_choice': 'Rent', 'list_SFFmFqOvH1Xv_choice_R6eScZwXzR0X': 'Sophie', 'number_oNYSbrj3CNlF': '10'}
class AddSplitwise(noOut):
      def __init__(self):
          self.gs = googleSheets.GoogleSheet('Actual Budget', '1I86sDhp4KS70ciAF7K7ufIZ68TqW0j2h-epFuRHYeYQ')
          self.sw = SplitWise("7cyClwYaOdlrwoPzL8uYtDLOwoJf9Efwj0ciLxgD", "r1YmAlIhQsojnhkyjRZZCXVPih7C90EELx2V4LgC")
          def addSplitwise(tf):
              amount = tf['number_oNYSbrj3CNlF']
              name = False
              if 'textfield_Maf3TeF00J84' in tf:
                 name = tf['textfield_Maf3TeF00J84']
              catagory = tf['list_uDy8LvuB3wTa_choice']
              split = [tf[i].lower() for i in tf.keys() if 'list_SFFmFqOvH1Xv_choice' in i]
               
              users = []
              namesfg = []
              if split:
                  for i in self.sw.getGroups():
                      if i.getName().lower() in split:
                         namefg.extend(i.getMembers())
                  split.extend(namesfg)
                  for i in self.sw.getFriends():
                      print(i.__dict__)
                      first = i.getFirstName()
                      if not first:
                         first = ""
                      last = i.getLastName()
                      if not last:
                         last = ""
                      if first.lower() + ' ' + last.lower() in split:
                         user = ExpenseUser()
                         user.setId(i.getId())
                         user.setPaidShare('0')
                         user.setOwedShare('1')
                         users.append(user)
                     
                  each = '%.2f'%(float(amount)/(len(users)+1))
                  for user in users:
                      user.setOwedShare(each)

                  me = ExpenseUser()
                  me.setId(self.sw.getCurrentUser().getId())
                  me.setOwedShare('%.2f'%(float(100*int(amount)-int(100*float(each)*len(users)))/100))
                  me.setPaidShare(amount)
                  users.append(me)
             
                  expense = Expense()
                  expense.setCost(str(amount))
                  expense.setDescription(name)
                  expense.setUsers(users)
                  print(users)
                  self.sw.createExpense(expense)

              row = self.gs.getRow(catagory)
              monYr = datetime.datetime.now().strftime("%b %Y")
              col = self.gs.getCol(monYr)

              self.gs.addCell(col, row, amount)
 
          super().__init__(addSplitwise)


############################
#######Google Sheets########
############################


class GetBlockDates(noIn):
      def __init__(self):
          self.gs = googleSheets.GoogleSheet('addWeeklyQuarterDates', '1jKEN0xOXZuIAMTumUYu8dW18VG3KjcWfmyFSvYfJQrs')
          def getBlockDates():
              names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "endDate"]
              def f(date):
                  date = re.findall('([0-9]+)[/-]([0-9]+)[/-]([0-9]+)', date)[0]
                  return datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
              return Item(set([]), {
                  "This" : dict(zip(names, [f(i) for i in self.gs.getRange("A", "17", "H", "17")[0]])),
                  "Next" : dict(zip(names, [f(i) for i in self.gs.getRange("A", "24", "H", "24")[0]])),
                  "Forever" : dict(zip(names, [f(i) for i in self.gs.getRange("A", "17", "G", "17")[0]]+[False]))
                  })
          super().__init__(getBlockDates)


############################
######Google Calendar#######
############################

class GetEvents(noIn):
      def __init__(self):
          self.cal = googleCalendar.GoogleCalendarGroup()
          def getEvents():
              x = self.cal.getCurrEvent()
              if x:
                 return Item([],x)
              else:  
                 return None
          super().__init__(getEvents)


#########################
#########Twilio##########
#########################

class SendSMS(noOut):
      def __init__(self, account_sid, auth_token, sendr, to):
          self.client = sms.Twilio(account_sid, auth_token, sendr, to)
          def sendSMS(withSMS):
              self.client.send(withSMS["SMS"])
          super().__init__(sendSMS)









from typeforms import *
from toDoist import *
from googleSheets import *
from googleCalendar import *
from machine import *
from testNodes import *
from realNodes import *
import pytz
from sms import *
from logicNodes import *

#creates the machine to orgenise workflows into
rpm = PreMachine()

#add this typeform to the amchine
gtf = getTypeform("Account string", 'Wie1UR')

rpm.addPreNode(gtf)

#get a set of dates
gbd = GetBlockDates()

rpm.addPreNode(gbd)

#when above typeform is completed add the results as a hw due date
rpm.addCnct(gtf, AddHwSeries(), 'tf')

#next typeform
gtf1 = getTypeform("Account string", 'Tryg7Q')
ac = AddClass()
rpm.addCnct(gtf1, ac, 'tf')
rpm.addCnct(gbd, ac, 'blockDate')

gtf2 = getTypeform("Account string", 'RYe9YL')

#two typeforms to add a project and its component parts
asp = AddSmallProj()
rpm.addCnct(gtf2, asp, 'tf')

#typeform to add a recuring event for a quarter
gtf3 = getTypeform("Account string", 'q9ZftZ')
arqe = AddRecuringQuarterEvent()
rpm.addCnct(gbd, arqe, 'blockDate')
rpm.addCnct(gtf3, arqe, 'tf')

#This workflow adds a wakeup message to send each day
ln = IsTitle("Wakeup")
orr = OR()
rpm.addCnct(GetEvents(), ln)
rpm.addCnct(ln, orr)
rpm.addCnct(retVal("SMS", "Brush teeth\nGetDressed\nSto Home Clothes\nWater plants\nFeed Lucy\nWalk Lucy\n Breakfast"), orr, 'y')
rpm.addCnct(orr, SendSMS("Account string",
              "Account string", "+18186964342", "+18188545107"), 'withSMS')

#This typeform adds a purchus to splitwise for tracking 
gtf3 = getTypeform("Account string", 'Xfywnm')
asw = AddSplitwise()
rpm.addCnct(gtf3, asw, 'tf')

#run the machine
ma = rpm.getMachine()
while (True):
  ma.run()
  sleep(60*5)


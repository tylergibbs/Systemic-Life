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


rpm = PreMachine()

gtf = getTypeform("d9676675560379280f2ae301ccac6537c44df100", 'Wie1UR')

rpm.addPreNode(gtf)

gbd = GetBlockDates()

rpm.addPreNode(gbd)

#Do typeforms
rpm.addCnct(gtf, AddHwSeries(), 'tf')

gtf1 = getTypeform("d9676675560379280f2ae301ccac6537c44df100", 'Tryg7Q')
ac = AddClass()
rpm.addCnct(gtf1, ac, 'tf')
rpm.addCnct(gbd, ac, 'blockDate')

gtf2 = getTypeform("d9676675560379280f2ae301ccac6537c44df100", 'RYe9YL')

asp = AddSmallProj()
rpm.addCnct(gtf2, asp, 'tf')

gtf3 = getTypeform("d9676675560379280f2ae301ccac6537c44df100", 'q9ZftZ')
arqe = AddRecuringQuarterEvent()
rpm.addCnct(gbd, arqe, 'blockDate')
rpm.addCnct(gtf3, arqe, 'tf')

ln = IsTitle("Wakeup")
orr = OR()
rpm.addCnct(GetEvents(), ln)
rpm.addCnct(ln, orr)
rpm.addCnct(retVal("SMS", "Brush teeth\nGetDressed\nSto Home Clothes\nWater plants\nFeed Lucy\nWalk Lucy\n Breakfast"), orr, 'y')
rpm.addCnct(orr, SendSMS("ACe2c4b47f9ff411c9f0b52bb49d264d1c",
              "86e36a18c9ddee320944bfe3c4a8b338", "+18186964342", "+18188545107"), 'withSMS')

gtf3 = getTypeform("d9676675560379280f2ae301ccac6537c44df100", 'Xfywnm')
asw = AddSplitwise()
rpm.addCnct(gtf3, asw, 'tf')

ma = rpm.getMachine()
while (True):
  ma.run()
  sleep(60*5)


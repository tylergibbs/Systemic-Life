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

"""
print("backend")
#googleCalendar
gc = GoogleCalendar('-------@group.calendar.google.com')
print("print gc.getCurrEvents")
print(len(gc.getCurrEvents()))
print("adding test event")
tz = pytz.timezone(gc.tz)
#gc.addEvent("test event", datetime.date(2018,4,25), datetime.datetime.now(tz).time(), 30)
print("add recuring event")
#gc.addEvent("test event recr", datetime.date(2018,4,25), datetime.datetime.now(tz).time(), 30, recur=True)
print("print gc.getCurrEvents")
print(len(gc.getCurrEvents()))
#gc.addEvent("test event1", datetime.datetime.now().date(), datetime.datetime.now(tz).time(), 30)
#gc.addEvent("test event2", datetime.datetime.now().date(), datetime.datetime.now(tz).time(), 30)
#gc.addEvent("test event3", datetime.datetime.now().date(), datetime.datetime.now(tz).time(), 30)
print(len(gc.getCurrEvents()))
print(gc.getCurrEvent())
print(gc.getCurrEvent())
print(gc.getCurrEvent())
print(gc.getCurrEvent())
print(gc.getCurrEvent())
print(gc.preEvents)
#googleSheets
gs = GoogleSheet('addWeeklyQuarterDates', '')
print('same range twice')
print('getRange')
print(gs.getRange('A', 1, 'E', 6))
print('getRangeNum')
print(gs.getRangeNum(1,1,5,6))
gs = GoogleSheet("Sheet1" ,"")
print('add range')
gs.updateRange('A', 1, 'B', 2, [[1,2],[3,4]])
print(gs.getRange('A', 1, 'B', 2))
v = gs.getCell('A',1)
gs.updateCell('A',1,'=' + str(v) + '+' + '1')
print(gs.getCell('A',1))
gs = GoogleSheet("Actual Budget" ,"")
print(gs.getCell('A',1))
#toDoist
td = Todoist('')
print('td.getProj(\'Home Logistics\')')
print(td.getProj('Home Logistics'))
print('td.getProjDue(\'Home Logistics\')')
print(td.getProjDue('Home Logistics'))
print("add test to home logistics")
tid = td.addTaskProj("test", 'Home Logistics')['id']
print("td.getProj('Home Logistics')")
print(td.getProj('Home Logistics'))
print("deleting task")
td.deleteTask(tid)
print("td.getProj('Home Logistics')")
print(td.getProj('Home Logistics'))
#print('all tasks')
#print(td.getTasks(TaskFillters.taskExists))


tf = Typeform('', ['Wie1UR'])
print("geting typforms each line should return one followed by pretypeforms")
print(tf.getTypeform())
print(tf.getPreTypeformIDs())
print(tf.getPreTypeformIDs())
print(tf.getPreTypeformIDs())
#Google Calendat group

gcg = GoogleCalendarGroup()

print(gcg.getCurrEvent())
print(gcg.getCurrEvent())
print(gcg.getCurrEvent())
print(gcg.getCurrEvent())
#twilio
twl = Twilio("", "", "+18186964342", "+18188545107")
twl.send("test msg")

print(twl.getMes())
"""



##########
###maps###
##########
"""
print("testmaps")

test = getTest()
rm = rmVal()
pr = printTest()

pm = PreMachine()
pm.addPreNode(test)
pm.addPreNode(rm)
pm.addPreNode(pr)

pm.cnctPreNodes(test.ID, rm.ID, 'x')
pm.cnctPreNodes(rm.ID, pr.ID, 'x')

print(pm.validMachine())
mach = pm.getMachine()
mach.run()
"""
"""
##########
test2 = getTest2()
rm2 = rmVal()
pr2 = printTest()

pm.addPreNode(test2)
pm.addPreNode(rm2)
pm.addPreNode(pr2) 

pm.cnctPreNodes(test2.ID, rm2.ID, 'x')
pm.cnctPreNodes(rm2.ID, pr2.ID, 'x')

print(pm.validMachine())
mach = pm.getMachine()
mach.run()
print('')

rmO = rmOR()
rmA = rmAND()

pr3 = printTest()
pr4 = printTest()

pm.addPreNode(rmO)
pm.addPreNode(rmA)
pm.addPreNode(pr3)
pm.addPreNode(pr4)

pm.cnctPreNodes(test.ID, rmO.ID, 'x')
pm.cnctPreNodes(test2.ID, rmO.ID, 'y')
pm.cnctPreNodes(test.ID, rmA, 'x')
pm.cnctPreNodes(test2.ID, rmA.ID, 'y')
pm.cnctPreNodes(rmO.ID, pr3.ID, 'x')
pm.cnctPreNodes(rmA, pr4.ID, 'x')

print(pm.validMachine())
mach = pm.getMachine()
mach.run()
"""

print("real maps")
rpm = PreMachine()

gtf = getTypeform("", 'Wie1UR')
#print inputs
"""pr5 = printTest()

rpm.addPreNode(gtf)
rpm.addPreNode(pr5)

rpm.cnctPreNodes(gtf, pr5, 'x')

gbd = GetBlockDates()
pr6 = printTest()

rpm.addPreNode(gbd)
rpm.addPreNode(pr6)
rpm.cnctPreNodes(gbd, pr6, 'x')

#Do typeforms
rpm.addCnct(gtf, AddHwSeries(), 'tf')

gtf1 = getTypeform("", 'Tryg7Q')
ac = AddClass()
rpm.addCnct(gtf1, printTest())
rpm.addCnct(gtf1, ac, 'tf')
rpm.addCnct(gbd, ac, 'blockDate')

gtf2 = getTypeform("", 'RYe9YL')

asp = AddSmallProj()
rpm.addCnct(gtf2, printTest())
rpm.addCnct(gtf2, asp, 'tf')
"""
gtf3 = getTypeform("", 'Xfywnm')
asw = AddSplitwise()
rpm.addCnct(gtf3, printTest())
rpm.addCnct(gtf3, asw, 'tf')

"""
gtf3 = getTypeform("", 'q9ZftZ')
arqe = AddRecuringQuarterEvent()
rpm.addCnct(gtf3, printTest())
rpm.addCnct(gbd, arqe, 'blockDate')
rpm.addCnct(gtf3, arqe, 'tf')

rpm.addCnct(GetEvents(), printTest())

rpm.addCnct(retValOne("SMS", "test message"), SendSMS("",
              "", "+18186964342", "+18188545107"), "withSMS")

ln = IsTitle("Wakeup")
orr = OR()
rpm.addCnct(GetEvents(), ln)
rpm.addCnct(ln, orr)
rpm.addCnct(retVal("SMS", "wakeup\ntest"), orr, 'y')
rpm.addCnct(orr, SendSMS("",
              "", "+18186964342", "+18188545107"), 'withSMS')
rpm.addCnct(GetEvents(), printTest())
rpm.addCnct(orr, printTest())
"""
ma = rpm.getMachine()
ma.run()
ma.run()

















from datetime import datetime
from twilio.rest import Client
import threading
import time

class Conver():
   def __init__(self, twilio, wait, termLim):
       self.client = twilio
       self.wait = wait
       self.termLim = termLim/wait
   def respond(self, message):
       return False
   def run(self):
       def f():
         mesIgnor = set([])
         termLim = self.termLim
         while termLim > 0:
           mes = self.client.getMes()
           if mes and mes not in mesIgnor:
             mesIgnor.add(mes)
             res = self.respond(mes)
             if not res:
                break
             else: 
                self.client.send(mes)
           time.sleep(wait)
           termLim -= 1
       threading.start_new_thread(f)

class Sequence(Conver):
      def __init__(self, messes, f, twilio, wait, termLim):
          self.meses = messes
          self.f = f
          super().__init__(twilio, wait, termLim)
      def respond(self, message):
          if message:
             f(message)
          if self.meses == []:
             return False
          else:
             ret = self.meses[0]
             self.meses = self.meses[1:]
             return ret

class Message(Sequence):
      def __init__(self, mes, twilio, wait, termLim):
          super().__init__([mes], lambda x: None, twilio, wait, termLim)

class Twilio():
   def __init__(self, account_sid, auth_token, sendr, to, wait = 10, termLim = 60*4):
       self.client = Client(account_sid, auth_token)
       self.sendr = sendr
       self.to = to
   def send(self, message):
       self.client.messages.create(
         to=self.to,
         from_ = self.sendr,
         body=message)
   def getMes(self):
       sms = sorted(self.client.messages.list(), key = lambda x: x.date_created, reverse=True)
       if sms:
          return sms[0].body
       else:
          return None


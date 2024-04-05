import datetime
import json
import requests
import time
from time import sleep

class Typeform():
      pre_typeform_file = "/home/crewmana/system2.5/PreTypeforms"
      time_btwn_calls = 60*5
      
      def __init__(self, api_key, typeform_ids):
          self.api_key = api_key
          self.typeform_ids = typeform_ids
          self.typeforms = []
      #Reads typeform form from a file describing the typeform 
      def getPreTypeformIDs(self):
          f = open(self.pre_typeform_file)
          l = f.readlines()
          f.close()
          return [x.split(" ")[0].strip() for x in l]
      #adds a typeform to typeform by id
      def addPreTypeformID(self, ID):
          now = str(datetime.datetime.now())
          f = open(self.pre_typeform_file,'a')
          f.write(ID + " " + now + '\n')
      #gets preTyepforms based on date and result
      def filterPreTypeforms(self):
          f = open(self.pre_typeform_file, 'r')
          l = f.readlines()
          f.close()
          f = open(self.pre_typeform_file, 'w')
          for i in l:
              if datetime.datetime.strptime(" ".join(i.split(" ")[1:]).split('.')[0].strip(), "%Y-%m-%d %H:%M:%S") \
                 > datetime.datetime.now() - datetime.timedelta(seconds = self.time_btwn_calls):
                 f.write(i)
          f.close()
      #pulls typeform answers from typeform.com that havent been pulled
      def getTypeformsWeb(self):
          request_template = "https://api.typeform.com/v1/form/{}?key={}&since={}"
          typeforms = []
          for typeform_id in self.typeform_ids:
              sleep(1/3)
              typeform = requests.get(request_template.format(typeform_id,\
                         self.api_key, time.time() - self.time_btwn_calls))
              #check if any new completed responces
              typeform = typeform.json()
              if "http_status" in typeform.keys():
                 for responce in typeform['responses']:
                     if responce["completed"] == '1':
                        typeforms.append((responce["token"], responce["answers"]))
          return typeforms
      #showes all current typeform results
      def getTypeforms(self):
          typeforms = self.getTypeformsWeb()
          preTypeforms = self.getPreTypeformIDs()
          return [i for i in typeforms if not i[0] in preTypeforms]
      #gets next typeform 
      def getTypeform(self):
          if self.typeforms==[]:
             self.filterPreTypeforms()
             self.typeforms = self.getTypeforms()
          if self.typeforms != []:
             ret = self.typeforms[0]
             self.addPreTypeformID(ret[0])
             self.typeforms = self.typeforms[1:]
             return ret[1]
          else:
             return False

          
              

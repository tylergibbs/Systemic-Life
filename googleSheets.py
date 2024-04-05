import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import pytz
import subprocess

class GoogleSheet:
      def __init__(self, sheetId, url):
          self.url = url
          self.sheetId = sheetId
          self.service = self.getService()
      #gets instance of google sheets api
      def getService(self):
         credentialDir = os.path.join(os.path.expanduser('~'), '.credentials')
         if not os.path.exists(credentialDir):
              os.makedirs(credentialDir)
         credential_path = os.path.join(credentialDir, 'sheets-python-life-manadgement.json')
         store = Storage(credential_path)
         credentials = store.get()
         if not credentials or credentials.invalid:
              flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
              flow.user_agent = APPLICATION_NAME
              credentials = tools.run_flow(flow, store)
              print('Storing credentials to ' + credential_path)
         discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
         http = credentials.authorize(httplib2.Http())
         return discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
      #creates a column 
      def genColName(self, num):
          ret = ''
          while num > 25:
              num -= 1
              val = num % 26
              num = num/26
              ret = chr(val+65) + ret
          if num >= 0:
             num -= 1
             val = num % 26 
             num = num/26
             ret = chr(val+65) + ret
          return ret
      #gets a rance of cells
      def getRangeNum(self, stRow, stCol, ndRow, ndCol):
          return self.getRange(self.genColName(int(stCol)), stRow, self.genColName(int(ndCol)), ndRow)
      #gets a range of cells by name
      def getRange(self, stRow, stCol, ndRow, ndCol):
          rangeName = self.sheetId + '!{}{}:{}{}'.format(stRow, stCol, ndRow, ndCol)
          print(rangeName)
          return self.service.spreadsheets().values().get(spreadsheetId=self.url, range=rangeName).execute()['values']
      #gets a specifc cell
      def getCell(self, row, col):
          return self.getRange(row, col, row, col)[0][0]
      #updates a range of cells
      def updateRange(self, stRow, stCol, ndRow, ndCol, newValues):
          rangeName = self.sheetId + '!{}{}:{}{}'.format(stRow, stCol, ndRow, ndCol)
          Body = {
               'values' : newValues,
          }
          return self.service.spreadsheets().values().update(
                      spreadsheetId=self.url, range=rangeName,
                      valueInputOption='USER_ENTERED', body=Body).execute()

      #updates a particular cell
      def updateCell(self, row, col, val):
          return self.updateRange(row, col, row, col, [[val]])
      #adds a function to a cell
      def funcCell(self, row, col, fmt):
          cell = self.getCell(row,col)
          if cell[0] == '=':
             cell = cell[1:]
          self.updateCell(row, col, '=' + fmt.format(cell))
      #creates a summation cell
      def addCell(self, row, col, num):
          self.funcCell(row, col, "{}+" + str(num))
      #col refers to value of collum to search
      def posCol(self, col, val):
          return self.getRange('', col, '', col)[0].index(val)+1
      #get position in a row of a value
      def posRow(self, row, val):
          return self.getRange(row, '', row, '').index([val])+1
      
      def getRow(self, val):
          return self.posRow('A', val)

      def getCol(self, val):
          return self.genColName(self.posCol(1, val))




import uuid
import inspect

def getArgs(func):
    return inspect.getargspec(func)[0]

#a pre machine allows the user to organize their workflow before starting it
class PreMachine():
      def __init__(self):
          self.allNodes = {}
      #adds a node
      def addPreNode(self, preNode):
          self.allNodes[preNode.ID] = preNode
      def cnctPreNodes(self, IDfrom, IDto, name):
          if not isinstance(IDfrom, int):
             IDfrom = IDfrom.ID
          if not isinstance(IDto, int):
             IDto = IDto.ID
          fr = self.allNodes[IDfrom]
          to = self.allNodes[IDto]
          fr.addOutput(IDto)
          to.addInput(name, IDfrom)
      def addCnct(self, frm, to, name = 'x'):
          if frm.ID not in self.allNodes:
             self.addPreNode(frm)
          if to.ID not in self.allNodes:
             self.addPreNode(to)
          self.cnctPreNodes(frm, to, name)
      def getMachine(self):
          if self.validMachine():
             return Machine(dict(zip(self.allNodes.keys(),[i.getNode() for i in self.allNodes.values()])))
          else:
             print("invalid Machine")
             [print(i.inp) for i in self.allNodes.values()]
             [print(i.out) for i in self.allNodes.values()]
             raise ValueError("invalid Machine")
      def validMachine(self):
          for node in self.allNodes.values():
              if not node.validMachine():
                 return False
          return True
      #def __str__(self):
          
#A machine is a PreMachine that is running 
class Machine():
      def __init__(self, nodes):
          self.allNodes = nodes
          self.startNodes = [i for i in self.allNodes.values() if i.isStart()]
      def run(self):
          for node in self.startNodes:
              node.run(self.allNodes)
          for node in self.allNodes.values():
              node.clear()
      
#every node has an Item
class Item():
      def __init__(self):
          self.tags = set([])
          self.content = None
      def __init__(self,tags,content):
          self.tags = set(tags)
          self.content = content
      def getTags(self):
          return self.tags
      def getContent(self):
          return self.content

#a node is a particular action the api can take
class Node():
      def __init__(self, ID, inpIdNames, efect, out):
          self.ID = ID
          self.inpIdName = inpIdNames
          self.inpNames = dict([(i,None) for i in inpIdNames.values()])
          self.out = out
          self.efect = efect
      def call(self, item, inputID, allNodes):
          #print("call " + str(item) + ' ' + self.inpIdName[inputID])
          self.addItem(item, inputID)
          return self.run(allNodes)
      def addItem(self, item, inputID):
          if inputID in self.inpIdName:
             name = self.inpIdName[inputID]
             if self.inpNames[name] == None:
                self.inpNames[name] = item
             else:
                raise ValueError("tried to input value from same node twice")
          else:
              raise ValueError("tried to input value from node not in input space")
      def run(self, allNodes):
          if None in self.inpNames.values():
             return False
          else:
             output = self.efect(self.inpNames)
             for i in self.out:
                 if i in allNodes.keys():
                    allNodes[i].call(output, self.ID, allNodes)
                 else:
                    raise ValueError("tried to add value to node not in allNodes")
             return True
      def clear(self):
          for i in self.inpNames:
              self.inpNames[i] = None
      def isStart(self):
         return self.inpNames == {}  
#Pre nodes are Nodes that are not yet active
class PreNode():
      def __init__(self, inpNames):
          self.ID = uuid.uuid4().int
          varnms = list(set([i.replace('_tags','').replace('_content','') for i in inpNames]))
          self.inp = dict([(i,None) for i in varnms])#name ID
          self.out = []
          self.noOut=False
          self.noIn=False
      def addInput(self, name, inputID):
          if self.noIn:
             return False
          if name in self.inp.keys():
             if self.inp[name] == None:
                self.inp[name] = inputID
                return True
             else:
                raise ValueError("tried to add value from same node twice " + str(name))
          else:
              raise ValueError("tried to add value from node not in input space " + str(name) + str(self.inp.keys()))
      def removeInput(self, name):
          if name in self.inp.keys():
             if self.inp[name] != None:
                self.inp[name] = None
             else:
                raise ValueError("tried to remove input when input was None")
          else:
              raise ValueError("tried to remove input from node not in input space")
      def addOutput(self, ID):
          if not noIn:
             return False
          self.out.append(ID)
      def doEfect(self, inputDict):
          raise ValueError("PreNode is default class") 
      def getNode(self):
          idName = dict(zip(self.inp.values(),self.inp.keys()))
          return Node(self.ID, idName, self.doEfect, self.out)
      def isStart(self):
          return self.inp == {}
      def validMachine(self):
          return not None in self.inp.values() 
#a filter applies logic to a workflow
class filter(PreNode):
      def __init__(self, fil):
          super().__init__(getArgs(fil))
          self.ret = getArgs(fil)[0].replace('_tags','').replace('_content','')
          self.fil = fil
      def doEfect(self, inputDict):
          d = {} 
          for i in inputDict:
              d[i+'_tags'] = inputDict[i].getTags()
              d[i+'_content'] = inputDict[i].getContent() 
          if self.fil(**d):
             return inputDict[self.ret]

    
#class addTags(PreNode):
 #     def __init__(self, tagify):
  #        varnms = getArgs(tagify)
   #       super().__init__(varnms)
    #       
     #     self.tagify = tagify
      #def doEfect(self, inputDict):
       #   d = {}
        #  for i in inputDict:
         #     d[i+'_tags'] = inputDict[i].getTags()
          #    d[i+'_content'] = inputDict[i].getContent()
          #return Item(**d)
#an api action best understood as an edit
class edit(PreNode):
      def __init__(self, efect):
          super().__init__(getArgs(efect))
          self.ret = getArgs(efect)[0].replace('_tags','').replace('_content','')
          self.efect = efect
      def doEfect(self, inputDict):
          d = {}
          for i in inputDict:
              d[i+'_tags'] = inputDict[i].getTags()
              d[i+'_content'] = inputDict[i].getContent()
          return self.efect(**d)
           
#general action
class action(PreNode): 
      def __init__(self, efect):
          super().__init__(getArgs(efect))
          self.efect = efect
      def doEfect(self, inputDict):
          d = {}
          for i in inputDict:
              d[i] = inputDict[i].getContent()
          return self.efect(**d)
#action with no output
class noOut(action):
      def __init__(self, efect):
          super().__init__(efect)
          self.noOut=True
#action with no input
class noIn(action):
      def __init__(self, efect):
          super().__init__(efect)
          self.noIn=True
#action with no input or output
class single(action):
      def __init__(self, efect):
          super().__init__(efect)
          self.noOut=True
          self.noIn=True



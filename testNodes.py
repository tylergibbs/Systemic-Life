from machine import *

class getTest(noIn):
      def __init__(self):
          def f():
              print("getTest Exicute")
              return Item([],{'one' : 1, 'val' : True})
          super().__init__(f)

class getTest2(noIn):
      def __init__(self):
          def f():
              print("getTest Exicute")
              return Item([],{'one' : 1, 'val' : False})
          super().__init__(f)

class rmVal(filter):
      def __init__(self):
          def f(x_tags, x_content):
              print("rmVal Exicute " + str(x_content['val']))
              return x_content['val']
          super().__init__(f)

class rmOR(filter):
      def __init__(self):
          def f(x_tags, x_content, y_tags, y_content):
              print("rmOR Exicute " + str(x_content['val'] or y_content['val']))
              return x_content['val'] or y_content['val']
          super().__init__(f)
class rmAND(filter):
      def __init__(self):
          def f(x_tags, x_content, y_tags, y_content):
              print("rmAND Exicute " + str(x_content['val'] and y_content['val']))
              return x_content['val'] and y_content['val']
          super().__init__(f)

class printTest(noOut):
      def __init__(self):
          super().__init__(lambda x: print(x))

class retVal(noIn):
      def __init__(self, var, retval):
         def f():
             return Item([], {var : retval})
         super().__init__(f)

class retValOne(noIn):
      def __init__(self, var, retval):
         self.do = True
         def f():
             if self.do:
                self.do = False
                return Item([], {var : retval})
         super().__init__(f)

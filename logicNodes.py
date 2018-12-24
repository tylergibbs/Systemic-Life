from machine import *
import datetime
import random

##############################
#######Typeform filters#######
##############################
class OnlyTypeforms(filter):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: "Typeform" in x_tags and and_(x_tags, x_content))

class OnlyAddHwSeries(OnlyTypeforms):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: x_content['token'] is 'Wie1UR')

class OnlyAddClass(OnlyTypeforms):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: x_content['token'] is 'Tryg7Q')

class OnlyCompleteSmallProj(OnlyTypeforms):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: x_content['token'] is 'FJX3mz')

class OnlyAddSmallProj(OnlyTypeforms):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: x_content['token'] is 'RYe9YL')

class OnlyRecuringQuarterEvent(OnlyTypeforms):
      def __init__(self, and_ = lambda x_tags, x_content: True):
          super().__init__(lambda x_tags, x_content: x_content['token'] is 'q9ZftZ')

##############################
#######Calendar filters#######
##############################

class IsTitle(filter):
      def __init__(self, name):
          super().__init__(lambda x_tags, x_content: name in x_content['summary'])

class ContainsWord(filter):
      def __init__(self, subst):
          super().__init__(lambda x_tags, x_content: subst in x_content['description'])

#############################
####### l  o  g  i  c #######
#############################

class OR(edit):
      def __init__(self):
          super().__init__(lambda x_tags, x_content, y_tags, y_content: 
                          Item(x_tags | y_tags, {**x_content, **y_content}))



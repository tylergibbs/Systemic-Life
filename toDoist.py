from todoist.api import TodoistAPI
import datetime

#gets only the useful tasks and highlights overdue tasks 
class TaskFillters():
      def defult(x):
          return True
      def taskExists(x):
          if 'checked' in x and 'is_deleted' in x and 'is_archived' in x:
             return x['checked'] == 0 and x['is_deleted']==0 and x['is_archived']==0
          else:
             return False
      def taskInProj(proj):
          def ret(x):
             if 'project_id' in x:
                return x['project_id']==proj and TaskFillters.taskExists(x)
             else:
                return False
          return ret
      def taskOverDue(x):
          if 'due_date_utc' in x and x['due_date_utc']:
             return datetime.datetime.strptime(x['due_date_utc'], '%a %d %b %Y %H:%M:%S %z').replace(tzinfo=None) <= datetime.datetime.utcnow()\
                    and TaskFillters.taskExists(x)
          else:
             return False
      def taskProjDue(proj):
          return lambda x: TaskFillters.taskOverDue(x) and TaskFillters.taskInProj(proj)(x)


class Todoist():
      def __init__(self, api_key):
          self.api = TodoistAPI(api_key)
      #gets the id of a progect
      def projToId(self, project):
          for proj in self.api.state['projects']:
              if proj['name'].strip() == project.strip():
                 return proj['id']
      #adds a task to a project
      def addTaskProj(self, name, project):
          self.api.sync()
          item = self.api.items.add(name, self.projToId(project))
          self.api.commit()
          return item
      #gets task by a given task filter
      def getTasks(self, fil=TaskFillters.defult):
          self.api.sync()
          return [i for i in self.api.state['items'] if fil(vars(i)['data'])]
      #gets a named project
      def getProj(self, proj):
          proj = self.projToId(proj)
          return self.getTasks(TaskFillters.taskInProj(proj))
      #gets the duedate of a project
      def getProjDue(self, proj):
          proj = self.projToId(proj)
          return self.getTasks(TaskFillters.taskProjDue(proj))
      #delets task
      def deleteTask(self, ID):
          self.api.sync()
          self.api.items.get_by_id(ID).delete()
          self.api.commit()
   

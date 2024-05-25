import manage
import os
import tempfile
import datetime
from enum import Enum
from typing import List
import json

# a project consists of an environment to share what you've done (which will be
# done in statements), make comments, notes, memos etc on other people's statements,
# tag your statements and color code them and so on. 
# on each task or statement you can post updates. 
#syncing it with trello?
#the project manager can assign people to tasks, and people can also declare that they volunteer. Don't worry about the logging for now.
#you can also start typing out each option to choose it.
#abstractness rate, a way to mark how big a task is and an easy way to track progress
# there are 3 spaces once you're in a project, the logging area, the tasks and the statements. 
# +in the tasks space once you have there are updates, progress, info on task, notes, archived notes, updates, and archived updates.
# +in each update there's teh update's description and the comments. 
#you may also have the ability to edit things. probably not though.

# in the logging place there's an updates view, a progress view, 
# marked as a percent done maybe?
# pro bono tasks
# tasks should be marked onto who does them. you can implement a simple point system but not lame, like github's thing maybe

# there's also a keybindings file where you can choose keybinds for everything.

#each update to a task is added in one bullet point. there's also notes for other stuff.
#there can also be a plans section for tasks

#a team-building exercise game you can play, maybe some for decisions, where you have to make clear the decision, goals, problems etc.

#~~indev notes~~
# an id, name for project
# members, their rank in the project, 
# methods for promotion/demotion, changing the name, special promotion to leader method, 
# saving
# an action template that takes the method and the user trying to do it and checks if they have the required rank. 
    # for this there's a list/string/whatever for each method (meant for users) that holds the ranks that can access that action. 
# a rank required for actions file, like in discord. by default there are higher ranks and lower ranks, but you can add special rules to for example dissallow leaders from doing this one thing. 
# making new ranks

#fix the notations, typehints

##the whole rank system may be more complicated than you thought. disclose; simplify or dismiss.
#for promotions, by default a higher rank can promote or demote lower ranks to lower ranks. 
#if you have extra time ook into overriding these. 

#updates will be formatted in bullet points, but you can give extra notes on each bullet. there's another space for seeing extra notes.

#~~to track progress~~: 
# each task has a progression bar the value of which is determined by subtasks. you can make updates on both tasks and subtasks.

 

class rank(Enum):
    guest = 0
    member = 1
    moderator = 2
    #how to make them able to add to these? maybe no need for that.
    admin = 3
    owner = 4

rank_requirements = {
    #not final. may implement tuples, for default requirements instaed.
    'addprojectmembers': 3
    #...
}


def deserialize_Update(dict1):
    pass
def deserialize_Task(dict1):
    pass
def deserialize_project(dict1):
    pass
class Project:
    def __init__(self, name:str, date, id:int, members = [], tasks = []):
        self.Name:str = name
        self.Date = date
        self.Id:int = id
        self.Members:list(tuple(manage.Client, rank)) = members # type: ignore
        self.Tasks:list(Task) = tasks # type: ignore #the ID will be the index in this list
    def AddMembers(self, rank=rank.guest, *members):
        for p in members:
            self.Members.append(p.UserName, rank)
    def printmembers(self):
        for p in self.Members:
            print(p.UserName)    
    def toJSON(self):
        return json.dumps(self, default=lambda obj: obj.__dict__,  sort_keys=True, indent = 4)
    def save_project(self, path=None):
        if path == None:
            path = f"{self.Name}.json"
        with open(path, 'w') as file:
            json.dump(self, file, default=lambda obj: obj.__dict__, sort_keys=True, indent = 4)
    def AddTask(self, t):
        self.Tasks.append(t)
    def PrintTasks(self, with_id = True):
        for i in self.Tasks:
            print(i)
        

    #TBI
    def load_project(self, path):
        with open(path, 'r') as file:
            pass
            # data = json.load(file)
            # for key, value in data.items():



class Task:
    #add feature: add deadline and progress
    def __init__(self, name, date, task_priority = 0, updates = []):
        self.Name = name
        self.Date = date
        self.TaskPriority = task_priority
        self.Updates = updates

    def add_update(self, update):
        self.Updates.append(update)

    def show_updates(self):
        for i in self.Updates:
            print(i)

class Update:
    def __init__(self, title, date, content, creator_id, notes=[], comments = []):
        self.Title = title
        self.Date = date
        self.Content = content
        self.CreatorID = creator_id 
        self.Notes = notes
        self.Comments = comments


    #add feature: editors for making text files (notes, comments, updates)
    def write_update_stdscr(self, user):
        pass
    def write_update_vim(self, user):
        pass

class Comment:
    def __init__(self, title, date, creator_id, content):
        self.Title = title
        self.Date = date
        self.CreatorID = creator_id
        self.Content = content
    
#TBI
def actIfPerm():
    pass
            

#for quick testing
def main():
        rn = datetime.datetime.now
        p1 = Project("test1", 1, 1)
        user1 = manage.User('michael', 12345)
        update1 = Update('test', str(rn()), 'today i tested this method. I then modified this update to see if it would work.', str(user1.ID))
        p1.AddMembers(user1)
        p1.printmembers()
        t1 = Task('get gud', str(rn()))
        t1.add_update(update1)
        p1.AddTask(t1)
        p1.save_project()
        p2 = Project('', 0, 0)
        p2.load_project('p1.json')   
        p2.printmembers()

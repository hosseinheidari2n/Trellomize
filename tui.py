import curses
import curses.textpad as textpad
import terminaltools
import tempfile
import os
import uuid
import json_formatting
import re
import datetime
import project
import manage
from time import sleep

class RestrictedTextbox(textpad.Textbox):
    def __init__(self, *args, **kwargs): ##how to add more kwargs to child classes?
        super().__init__(*args, **kwargs)
        self.win.border()
        self.thingtypeded = [] # for debug
        self.typedstr = ''
        
    def do_command(self, char):
        '''checks if an action involves stepping outside of the confines of the dedicated box, allows it otherwise.'''
        y, x = self.win.getyx()[0] + 1, self.win.getyx()[1] + 1
        if char in (263,):
            if x == 2:
                if y == 2:
                    return True
                self.win.move(y - 2, self.maxx)   
            self.win.addstr('\b \b')
            self.typedstr = self.typedstr[:-1]
            return True
        elif char in (10,):
            if y == self.maxy:
                return True
            else:
                self.win.move(y, 1)
                self.typedstr = self.typedstr + '\n'
                return True
        else:
            self.thingtypeded.append(char)
            if x in (self.maxx + 1,):
                if y == self.maxy:
                    return True
                self.win.move(y, 1)
                self.typedstr = self.typedstr + '\n'
            if char != 7:
                self.typedstr = self.typedstr + chr(char)
        return super().do_command(char)
    
    def getstr(self):
        return self.typedstr
    
    def getthingtypeded(self):
        return self.thingtypeded
    

class Menu:
    def __init__(self, stdscr, options):
        self.stdscr = stdscr
        self.options = options
        self.current_index = 0
        self.typed_str = ''
        self.stdscr.clear()
        self.valid_options = []
        self.valid_index = 0

    # prompts an interface to terminal for choosing an option from a list    
    def display_options(self):
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            x = 0
            y = index
            if index == self.current_index:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x, option)
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, option)
        self.stdscr.refresh()

    def check_valid_options(self):
        self.valid_options.clear()
        for index, option in enumerate(self.options):
            option = option.lower()
            if re.match(f".*{self.typed_str}.*", option):
                self.valid_options.append((index, option))
        self.valid_index = 0        
    def run(self):
        self.stdscr.refresh()
        while True:
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.current_index = (self.current_index - 1) % len(self.options)
            elif key == curses.KEY_DOWN:
                self.current_index = (self.current_index + 1) % len(self.options)
            elif key in (curses.KEY_ENTER, 10) :
                self.stdscr.clear()
                self.stdscr.refresh()
                return self.current_index
            elif key in (9, ):
                if len(self.valid_options):
                    self.valid_index = (self.valid_index + 1)%len(self.valid_options)
                    self.current_index = self.valid_options[self.valid_index][0]
            else:
                #incomplete
                    #notes on completion: maybe a typing state it goes to, which can be exited when you know?
                    #bugs: cant type after tab, also no support for none character inputs
                #you can also start typing out an option to point the cursor to it.
                self.typed_str = self.typed_str + chr(key)
                self.check_valid_options()
                
                #here maybe add a feature where pressing tab lets you cycle through valid optoins.   
                if len(self.valid_options) == 0:
                    self.typed_str = '' + chr(key)
                    self.check_valid_options()
                    if len(self.valid_options) != 0:
                        self.current_index = self.valid_options[self.valid_index][0] 
                else:
                    self.current_index = self.valid_options[self.valid_index][0]    
            self.display_options()

#incomplete
def take_input(stdscr, y = None, x = None, height = None, width = None, clear = False):
    if clear: 
        stdscr.clear()
    text_win = curses.newwin(height, width, y + 1, x + 1)
    curses.textpad.rectangle(stdscr, y, x, y + height + 1, x + width + 1)
    box = curses.textpad.Textbox(text_win)
    stdscr.refresh()
    box.edit()
    return box.gather()
    
def view_project_tasks(stdscr, proj, user):
    if user.ID == proj.CreatorID:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Press M to Configure Members.')
        if stdscr.getch() == ord('m'):
            stdscr.addstr(0, 0, 'Enter a Username to add or remove.')
            username = input_box(stdscr, 1, 0, 1, 15)
            if not os.path.exists(f'users/{username}.json'):
                stdscr.clear()
                stdscr.addstr(0, 0, 'No Such User Found.')
                stdscr.getch()
            else:
                proj.Members.append(json_formatting.deserialize_dict_user(json.load(open(f'users/{username}.json', 'r'))))
                
            
    if user.ID != proj.CreatorID:
        stdscr.clear()
        task_list = [t.Name + ' | ' + str(t.Date) + ' | ' + str(t.DueDate) + ' | ' + str(states(t.State)) +  ' | ' +str(priorities(t.TaskPriority))  for t in proj.Tasks]
        c = Menu(task_list).run()
        task = proj.Tasks[c]
        view_task_admin(stdscr, task, user, proj)
    else:
        stdscr.clear()
        task_list = ['New Task'] + [t.Name + ' | ' + str(t.Date) + ' | ' + str(t.DueDate) + ' | ' + str(states(t.State)) +  ' | ' +str(priorities(t.TaskPriority))  for t in proj.Tasks]
        c = Menu(stdscr, task_list).run()
        if c == 0:
            proj.Tasks.append(take_task(stdscr, user))
        else:
            task = proj.Tasks[c-1]
            view_task_admin(stdscr, task, user, proj)
    
def goodnow():
    return str(datetime.datetime.now().date()) + ' ' +  str(datetime.datetime.now().time()).split(sep='.')[0]

#incomplete
def take_update(stdscr, user = None, date = goodnow()):
    stdscr.clear()
    pretitle = pretitle_arg
    pretext = pretext_arg
    while True:
        stdscr.addstr(1, 3, str(date), curses.color_pair(1))
        curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
        curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
        text_win = curses.newwin(37, 95, 7, 11)
        if pretext != None:
            stdscr.addstr(7, 11, pretext)
            stdscr.refresh()
        if titlemode:
            stdscr.addstr(5, 12, 'Choose a title: ' + ' ' * 20, curses.A_BOLD)
            title_win = curses.newwin(1, 25, 5, 27)
            title_box = curses.textpad.Textbox(title_win)
            stdscr.refresh()
            title_box.edit()
            title = title_box.gather().center(94)
            pretitle = title
        else:
            title = pretitle.center(94)
        stdscr.addstr(5, 12, title, curses.A_BOLD)
        if editmode:
            stdscr.refresh()
            box.edit()
            text = box.gather() 
        stdscr.addstr(47, 10, 'S: SAVE | E: EDIT | R: RESET | T: CHANGE TITLE')
        while True:
            c = stdscr.getch()  
            if c == ord('s'):
                return project.Update(title, date, text, creator_id)
            elif c == ord('e'):
                editmode = True
            elif c == ord('r'):
                pretext = None
                pretitle = None
                titlemode = True
                editmode = True
            elif c == ord('t'):
                titlemode = True
                editmode = False
            break

def take_comment(stdscr, creator_id = None, date = goodnow(), pretitle_arg = None, pretext_arg = None, editmode = False, titlemode = False):
    stdscr.clear()
    pretitle = pretitle_arg
    pretext = pretext_arg
    editmode = pretext == None
    titlemode = pretitle == None
    
    while True:
        stdscr.addstr(1, 3, str(date), curses.color_pair(1))
        curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
        curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
        text_win = curses.newwin(37, 95, 7, 11)
        if pretext != None:
            text_win.addstr(0, 0, pretext)
            stdscr.refresh()
        if titlemode:
            stdscr.addstr(5, 12, 'Choose a title: ' + ' ' * 20, curses.A_BOLD)
            title_win = curses.newwin(1, 25, 5, 27)
            title_box = curses.textpad.Textbox(title_win)
            stdscr.refresh()
            title_box.edit()
            title = title_box.gather().center(94)
            pretitle = title
        else:
            title = pretitle.center(94)
        stdscr.addstr(5, 12, title, curses.A_BOLD)
        if editmode:
            stdscr.refresh()
            box = curses.textpad.Textbox(text_win)
            box.edit()
            text = box.gather() 
        stdscr.addstr(47, 10, 'S: SAVE | E: EDIT | R: RESET | T: CHANGE TITLE')
        while True:
            c = stdscr.getch()  
            if c == ord('s'):
                return project.Comment(title, date, creator_id, text)
            elif c == ord('e'):
                editmode = True
            elif c == ord('r'):
                pretext = None
                pretitle = None
                titlemode = True
                editmode = True
            elif c == ord('t'):
                titlemode = True
                editmode = False
            break
        
def input_box(stdscr, y, x, height, width):
    text_win = curses.newwin(height, width, y, x)
    text_box = curses.textpad.Textbox(text_win)
    text_box.edit()
    return text_box.gather()

def take_task(stdscr, user = None, date = goodnow(), pretitle = None, pretext = None, members = [], preduedate = None, editmode = False, titlemode = False, duedatemode = False):
    member_assignments = []
    for m in members:
        member_assignments.append(False)
    text = str(pretext)
    editmode = pretext == None
    titlemode = pretitle == None
    duedatemode = preduedate == None
    while True:
        stdscr.clear()
        stdscr.addstr(1, 3, str(date), curses.color_pair(1))
        curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
        curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
        text_win = curses.newwin(37, 95, 7, 11)
        if pretext != None:
            text_win.addstr(0, 0, pretext)
            stdscr.refresh()
        box = curses.textpad.Textbox(text_win)
        stdscr.refresh()
        if titlemode:
            stdscr.addstr(5, 12, 'Choose a title: ' + ' ' * 20, curses.A_BOLD)
            title_win = curses.newwin(1, 25, 5, 27)
            title_box = curses.textpad.Textbox(title_win)
            stdscr.refresh()
            title_box.edit()
            title = title_box.gather().center(94)
            pretitle = title
        else:
            title = pretitle.center(94)
        stdscr.addstr(5, 12, title, curses.A_BOLD)
        if duedatemode:
            stdscr.addstr(0, 35, f'Due Date: ')
            a = str(input_box(0, 45, ))
            if not ('.' in a or ':' in a or ',' in a):
                duedate = datetime.datetime.now() + datetime.timedelta(days=1)
                duedate = str(duedate.date()) + ' ' +  str(duedate.time()).split(sep='.')[0]
            
        for i in range(len(members)):
            stdscr.addstr(7 + i, 130, members[i] + (' -ASSIGNED-' if member_assignments[i] else ' -UNASSIGNED-'))
        stdscr.refresh()
        if editmode:
            stdscr.refresh()
            box.edit()
            text = box.gather() 
        stdscr.addstr(47, 10, 'S: SAVE | M: CHOOSE MEMBERS | E: EDIT | R: RESET | T: CHANGE TITLE | D: CONFIGURE DUE DATE')
        while True:
            c = stdscr.getch()  
            if c == ord('s'):
                stdscr.clear()
                stdscr.addstr(0, 0, 'How important is this task? ')
                stdscr.getch()
                priority = Menu(stdscr, ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']).run()
                member_perms = [members[i] for i in range(len(members))]
                return project.Task(title, date, uuid.uuid1(), text, member_perms, priority)
            elif c == ord('m'):
                if members == None:
                    stdscr.addstr(0, 0, 'There are no members defined.')
                    stdscr.getch()
                else:
                    options = []
                    for i in range(len(members)):
                        options.append(members[i] + (' -ASSIGNED-' if member_assignments[i] else ''))
                    choice = Menu(stdscr, options).run()
                    member_assignments[choice] = not member_assignments[choice]
            elif c == ord('e'):
                editmode = True
            elif c == ord('r'):
                pretext = None
                pretitle = None
                editmode = True
            elif c == ord('t'):
                titlemode = True
                editmode = False
            elif c == ord('d'):
                duedatemode = True
                editmode = False
            break 

def view_update_admin(stdscr, update, user):
    #view update content, comments on the top right, notes on the bottom right. a button for adding comment / notes.
    
    stdscr.clear()
    stdscr.addstr(1, 3, str(update.Date), curses.color_pair(1))
    curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
    curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
    stdscr.addstr(5, 12, str(update.Title).center(94), curses.A_BOLD)
    stdscr.addstr(7, 12, str(update.Content))
    stdscr.addstr(47, 10, 'V: VIEW COMMENTS | C: ADD COMMENT')
    stdscr.refresh()
    c = stdscr.getch()
    if c == ord('c'):
        update.Comments.append(take_comment(stdscr, user.ID))
    elif c == ord('v'):
        view_comments(stdscr, update)

def view_comments(stdscr, update, user):
    names = [c.Title + ' | ' + str(c.CreatorID) + ' | ' + str(c.Date)  for c in update.Comments]
    names.insert(0, 'New Comment')
    stdscr.clear()
    c = Menu(stdscr, names).run()
    if c == 0:
        update.Comments.append(take_comment(stdscr, user.ID))
    else:
        stdscr.clear()
        comment = update.Comments[c-1]
        stdscr.addstr(1, 3, str(comment.Date), curses.color_pair(1))
        curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
        curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
        stdscr.addstr(5, 12, str(comment.Title).center(94), curses.A_BOLD)
        stdscr.addstr(7, 12, str(comment.Content))
        stdscr.refresh()
        stdscr.getch()
    
def view_task_admin(stdscr, task, user, proj):
        #shows all updates, their creator, date, members assigned and their assignment type, and a button for editing members or task info.
        stdscr.clear()
        stdscr.addstr(1, 3, str(task.Date), curses.color_pair(1))
        curses.textpad.rectangle(stdscr, 4, 10, 45, 106)
        curses.textpad.rectangle(stdscr, 4, 10, 6, 106)
        stdscr.addstr(5, 12, str(task.Name).center(94), curses.A_BOLD)
        stdscr.addstr(8, 11, task.Desc)
        stdscr.addstr(47, 10, 'U: VIEW UPDATES | M: VIEW MEMBERS' + (' | A: ADD UPDATE' if user.Username in task.Member_Perms else ''))
        stdscr.refresh()
        while True:
            c = getch()
            if c == ord('u'):
                stdscr.clear()
                c2 = Menu(stdscr, [u.Title for u in task.Updates]).run()
                view_update_admin(stdscr, task.Updates[c2], user)
            elif c == ord('m'):
                if user.ID == proj.CreatorID:
                    a = []
                    for i in range(len(proj.Members)):
                        a.append(7 + i, 8, proj.Members[i].Username + (' -ASSIGNED- ' if proj.Members[i].Username in task.Member_Perms else ''))
                    c = Menu(stdscr, a).run()
                    if proj.Members[c].Username in task.Member_Perms:
                        task.Member_Perms.remove(proj.Members[c].Username)
                    else:
                        task.Member_Perms.append(proj.Members[c].Username)
                else:
                    stdscr.clear()
                    for i in range(len(proj.Members)):
                        stdscr.addstr(7 + i, 8, proj.Members[i].Username + (' -ASSIGNED- ' if proj.Members[i].Username in task.Member_Perms else ''))
            elif c == ord('a'):
                if user.Username not in task.Member_Perms:
                    continue
                task.Updates.append(take_update(stdscr, user))
                
                
                
                
                
            
            

#for testing purposes
def main(stdscr):
    curses.start_color()
    curses.init_pair(1, 243, curses.COLOR_BLACK)
    curses.curs_set(0)
    # main_menu_options = ['Create manager', 'Login as manager', 'delete manager', 'Create user', 'Login as user']
    # main_menu = Menu(stdscr, main_menu_options)
    # current_menu = main_menu
    # print(current_menu.run())
    c1 = take_comment(stdscr, '11')
    p1 = project.Update('aaaa', 'today, ', 'bruh', '1', [], [project.Comment('a', 'now,', '1', 'aaaaaaa'), project.Comment('b', 'now,', '1', 'bbbbbbbbbbbbbb'), c1])
    # view_comments(stdscr, u1, manage.User('a', 'a', '12'))
    view_update_admin(stdscr, p1, manage.User('a', 'a', '12'))
    
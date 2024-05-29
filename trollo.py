import json
import manage
import tui
import project
import uuid
import curses
import os
import json_formatting
import datetime
from curses.textpad import *

if not os.path.isfile('logs/userlog.txt'):
    try:
        os.makedirs('logs')
    except FileExistsError:
        pass
    with open('logs/userlog.txt', 'w') as file:
        pass
LOGPATH_U = 'logs/userlog.txt'


def list_files(path):
    '''returns a list of all sub-paths in a directory as text'''
    list1 = []
    for r, useless, files in os.walk(path):
        for file in files:
            list1.append(os.path.join(r, file).replace('\\', '/'))
    return list1


def projectlist_notmine(stdscr, user):
    '''returns a list of projects in which the user is a member of'''
    plist = []
    for p in list_files('projects'):
        with open(p, r) as file:
            pdict = json.load(file)
        proj = json_formatting.deserialize_dict_project(pdict)
        if user.UserName in proj.Members:
            plist.append()
    return plist

    
def projectlist_notmine_names(stdscr, user):
    '''returns the name of projects in which the user is a member of'''
    names = []
    for p in projectlist_notmine(stdscr, user):
        names.append(p.Name)
    return names


def goodnow():
    '''a usable format of the datetime now() function'''
    return str(datetime.datetime.now().date()) + ' ' +  str(datetime.datetime.now().time()).split(sep='.')[0]


def save_project(stdscr, proj):
    '''saves a project object as json object'''
    with open(f'projects/{proj.Name}.json', 'w') as file:
        json.dump(proj, file, default= lambda o: o.__dict__)

    
def get_user_projects_names(stdscr, user_id):
    '''returns the list of projects saved under a user's id'''
    if not file_exists(f'projects/{user_id}'):
        return []
    try:
        return os.listdir(f'projects/{user_id}')
        # return [file for file in os.listdir(f'projects/{user_id}') if os.path.isfile(os.path.join('projects/{user_id}'), file)]
    except OSError:
        raise Exception(f'Error: failed to access path "projects/{user_id}"')


def file_exists(path):
    '''returns true if a file path exists.'''
    return os.path.exists(path)


def input_box(stdscr, y, x, height, width):
    text_win = curses.newwin(height, width, y, x)
    text_box = Textbox(text_win)
    text_box.edit()
    return text_box.gather().strip()


def UserInterface(stdscr, user):
    stdscr.clear()
    c2 = tui.Menu(stdscr, ['Create New Project', 'Load My Own Project', 'Load Project As Member']).run()
    if c2 == 0:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Enter a name for your project: ')
        stdscr.refresh()
        pname = input_box(stdscr, 1, 0, 1, 15)
        if not file_exists(f'projects/{user.ID}'):
            os.makedirs(f'projects/{user.ID}')
        if file_exists(f'projects/{user.ID}/{pname}.json'):
            stdscr.clear()
            stdscr.addstr(0, 0, 'A project with that name already exists. ')
            stdscr.getch()
        else:
            proj = project.Project(pname, goodnow(), user.ID)
            proj.Members.append(user)
            with open(f'projects/{user.ID}/{pname}.json', 'w') as file:
                json.dump(proj, file, default = lambda x: x.__dict__)
            stdscr.clear()
            stdscr.addstr(0, 0, 'New Project Created Successfully! ')
            stdscr.getch()
        
    elif c2 == 1:
        stdscr.clear()
        project_names = get_user_projects_names(stdscr, user.ID)
        if len(project_names) == 0:
            stdscr.clear()
            stdscr.addstr(0, 0, 'You have no project saved. Please create a project first.')
            stdscr.refresh()
            stdscr.getch()
            return
        str_cp = project_names[tui.Menu(stdscr, project_names).run()]
        with open(f'projects/{user.ID}/{str_cp}', 'r') as file:
            proj = json_formatting.deserialize_dict_project(json.load(file))
        tui.view_project_tasks(stdscr, proj, user)
        with open(f'projects/{user.ID}/{str_cp}', 'w') as file:
            json.dump(proj, file, default = lambda x: x.__dict__)
            
    elif c2 == 2:
        stdscr.clear()
        pnames = projectlist_notmine_names(stdscr, user)
        if len(pnames) == 0:
            stdscr.clear()
            stdscr.addstr(0, 0, 'You are not a member of any project.')
            stdscr.refresh()
            stdscr.getch()
            return
            
        tui.view_project_tasks(stdscr, projectlist_notmine(stdscr, user)[tui.Menu(stdscr, pnames).run()])
        

#~~~~~~~~~~~~~~~~
def main(stdscr):
    current_user = None
    logfile = open(LOGPATH_U, 'a')
    while True:
        if current_user == None:
            c1 = tui.Menu(stdscr, ['New User', 'Login']).run()
            if c1 == 0:
                stdscr.clear()
                stdscr.addstr(0, 0, 'Choose a Username: ')
                stdscr.refresh()
                username = input_box(stdscr, 1, 0, 1, 15)
                while True:
                    stdscr.clear()
                    stdscr.addstr(0, 0, 'Choose a Password: ')
                    stdscr.refresh()
                    password = input_box(stdscr, 1, 0, 1, 25)
                    stdscr.addstr(3, 0, 'Confirm Password: ')
                    stdscr.refresh()
                    cpassword = input_box(stdscr, 4, 0, 1, 25)
                    if (cpassword != password):
                        stdscr.clear()
                        stdscr.addstr(0, 0, 'The Passwords didn\'t match. You might\'ve made a typo! Please try again.')
                        stdscr.getch()
                    else:
                        stdscr.clear()
                        generated_id = str(uuid.uuid1())
                        logfile.write(f'Created User: {username} - {generated_id}\n')
                        stdscr.addstr(0, 0, 'User Created Successfully! ')
                        stdscr.getch()
                        break
                with open(f'users/{username}.json', 'w') as file:
                    json.dump(manage.User(username, manage.HashPassword(password), generated_id), file, default=lambda o: o.__dict__)
                continue
                
            elif c1 == 1:
                while True:
                    stdscr.clear()
                    stdscr.addstr(0, 0, 'Enter your Username: ')
                    stdscr.refresh()
                    username = input_box(stdscr, 1, 0, 1, 15)
                    if not file_exists(f'users/{username}.json'):
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'No user found with the username: {username}')
                        stdscr.getch()
                    stdscr.clear()
                    stdscr.addstr(0, 0, 'Enter your Password: ')
                    stdscr.refresh()
                    password = input_box(stdscr, 1, 0, 1, 25)
                    u_dict = json.load(open(f'users/{username}.json', 'r'))
                    current_user = manage.User(u_dict['UserName'], u_dict['Password'], u_dict['ID'])
                    if (manage.CalculateHash(password) != current_user.Password):
                        stdscr.clear()
                        stdscr.addstr(0, 0, 'Password Incorrect')
                        stdscr.getch()
                        continue
                    stdscr.clear()
                    stdscr.addstr(0, 0, f'Welcome, {current_user.UserName}!')
                    logfile.write(f'User login: {username}\n')
                    stdscr.getch()
                    break
        else:
            c10 = tui.Menu(stdscr, ['View Projects', 'logout']).run()
            if c10 == 0:
                UserInterface(stdscr, current_user)
            elif c10 == 1:
                logfile.write(f'User logout: {current_user.UserName}\n')
                current_user = None

                
curses.wrapper(main)
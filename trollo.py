import json
import manage
import tui
import project
import uuid
import curses
import os
import json_formatting
import datetime
uuid
from curses.textpad import *

allow = True
LOGPATH_U = 'logs/userlog.txt'

def goodnow():
    return str(datetime.datetime.now().date()) + ' ' +  str(datetime.datetime.now().time()).split(sep='.')[0]

def save_project(stdscr, proj):
    with open(f'projects/{proj.Name}.json', 'w') as file:
        json.dump(proj, file, default= lambda o: o.__dict__)

def view_project_tasks(stdscr, proj, user):
    stdscr.clear()
    task_list = [t.Name + ' | ' + str(t.Date) + ' | ' + str(t.DueDate) + ' | ' + str(states(t.State)) +  ' | ' +str(priorities(t.TaskPriority))  for t in proj.Tasks]
    c = tui.Menu(task_list).run()
    task = proj.Tasks[c]
    tui.view_task_admin(stdscr, task, user, proj)
    
def get_user_projects_names(stdscr, user_id):
    try:
        return os.listdir(f'projects/{user_id}')
        # return [file for file in os.listdir(f'projects/{user_id}') if os.path.isfile(os.path.join('projects/{user_id}'), file)]
    except OSError:
        raise Exception(f'Error: failed to access path "projects/{user_id}"')

def file_exists(path):
    return os.path.exists(path)

def input_box(stdscr, y, x, height, width):
    text_win = curses.newwin(height, width, y, x)
    text_box = Textbox(text_win)
    text_box.edit()
    return text_box.gather()

def UserInterface(stdscr, user):
    stdscr.clear()
    c2 = tui.Menu(stdscr, ['Create New Project', 'Load Project']).run()
    if c2 == 0:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Enter a name for your project: ')
        pname = input_box(stdscr, 1, 0, 1, 15)
        if not file_exists(f'projects/{user_id}'):
            os.mkdir(f'projects/{user_id}')
        if file_exists(f'projects/{user.ID}/{pname}.json'):
            stdscr.clear()
            stdscr.addstr(0, 0, 'A project with that name already exists. ')
            stdscr.getch()
        else:
            proj = project.Project(pname, goodnow(), user.ID)
            with open(f'projects/{user.ID}/{pname}.json', 'w') as file:
                json.dump(proj, file, default = lambda x: x.__dict__)
            stdscr.clear()
            stdscr.addstr(0, 0, 'New Project Created Successfully! ')
            stdscr.getch()
        
    elif c2 == 1:
        stdscr.clear()
        project_names = get_user_projects_names(stdscr, user.ID)
        str_cp = project_names[tui.Menu(stdscr, project_names).run()]
        with open(f'projects/{user.ID}/{str_cp}', 'r') as file:
            proj = json_formatting.deserialize_dict_project(json.load(file))
        tui.view_project_tasks(stdscr, proj, user)

def main(stdscr):
    current_user = None
    with open(LOGPATH_U, 'a') as logfile:
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
                            logfile.write(f'Created User: {username} - {generated_id}')
                            stdscr.addstr(0, 0, 'User Created Successfully! ')
                            stdscr.getch()
                            break
                    with open(f'users/{username}.json', 'w') as file:
                        json.dump(manage.User(username[:-1], manage.HashPassword(password[:-1]), generated_id), file, default=lambda o: o.__dict__)
                    continue
                    
                elif c1 == 1:
                    stdscr.clear()
                    stdscr.addstr(0, 0, 'Enter your Username: ')
                    stdscr.refresh()
                    username = input_box(stdscr, 1, 0, 1, 15)
                    if not file_exists(f'users/{username}.json'):
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'No user found with the username: {username}')
                        stdscr.getch()
                    while True:
                        stdscr.clear()
                        stdscr.addstr(0, 0, 'Enter your Password: ')
                        stdscr.refresh()
                        password = input_box(stdscr, 1, 0, 1, 25)
                        u_dict = json.load(open(f'users/{username}.json', 'r'))
                        current_user = manage.User(u_dict['UserName'], u_dict['Password'], u_dict['ID'])
                        if (manage.CalculateHash(password) != current_user.Password) and not allow:
                            stdscr.clear()
                            stdscr.addstr(0, 0, 'Password Incorrect')
                            stdscr.getch()
                            continue
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'Welcome, {current_user.UserName}!')
                        stdscr.getch()
                        break
            else:
                c10 = tui.Menu(stdscr, ['View Projects', 'logout']).run()
                if c10 == 0:
                    UserInterface(stdscr, current_user)
                elif c10 == 1:
                    current_user = None
                    
                    
                    
                    

                
curses.wrapper(main)
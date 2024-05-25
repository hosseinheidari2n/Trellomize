import curses
import curses.textpad as textpad
import terminaltools
import tempfile
import os
import re
import datetime
from time import sleep

class RestrictedTextbox(textpad.Textbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win.border()
        self.thingtypeded = [] # for debug
        
    def do_command(self, char):
        '''checks if an action involves stepping outside of the confines of the dedicated box, allows it otherwise.'''
        y, x = self.win.getyx()[0] + 1, self.win.getyx()[1] + 1
        if char in (263,):
            if x == 2:
                if y == 2:
                    return True
                self.win.move(y - 2, self.maxx)   
            self.win.addstr('\b \b')
            return True
        else:
            if x in (self.maxx + 1,):
                if y == self.maxy:
                    return True
                self.win.move(y, 1)
        return super().do_command(char)
    
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
    text_win = curses.newwin(y, x, height, width)
    text_win.move(1, 1)
    box = RestrictedTextbox(text_win, False)
    box.edit()
    print(box.getthingtypeded())
    sleep(10)
    return box.gather()

#incomplete
def take_update(stdscr, user, date = str(datetime.datetime.now().date()) + ' ' +  str(datetime.datetime.now().time()).split(sep='.')[0]):
    stdscr.clear()
    maxx, maxy = stdscr.getmaxyx()
    stdscr.addstr(1, maxx//8, str(date), curses.color_pair(1))
    take_input(stdscr, 10, 10, 10, 10)
    stdscr.refresh()
    sleep(5)
    
    
#for testing purposes
def main(stdscr):
    curses.start_color()
    curses.init_pair(1, 243, curses.COLOR_BLACK)
    curses.curs_set(0)
    # main_menu_options = ['Create manager', 'Login as manager', 'delete manager', 'Create user', 'Login as user']
    # main_menu = Menu(stdscr, main_menu_options)
    # current_menu = main_menu
    # print(current_menu.run())
    take_update(stdscr, None)
curses.wrapper(main)
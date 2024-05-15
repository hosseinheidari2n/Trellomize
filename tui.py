import curses
import terminaltools
import tempfile
import os
import re

class Menu:
    def __init__(self, stdscr, options):
        self.stdscr = stdscr
        self.options = options
        self.current_index = 0
        self.typed_str = ''
        self.stdscr.clear()
        self.valid_options = []
        self.valid_index = 0

    #prints options, with reversed (white background, black text) colors if chosen.    
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
                return self.next_menu
            elif key in (9, ):
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
                    self.current_index = self.valid_options[self.valid_index][0] 
                else:
                    self.current_index = self.valid_options[self.valid_index][0]    
            self.display_options()

def main(stdscr):
    curses.curs_set(0)
    main_menu_options = ['Create manager', 'Login as manager', 'delete manager', 'Create user', 'Login as user']
    main_menu = Menu(stdscr, main_menu_options)
    current_menu = main_menu

    while current_menu:
        current_menu = current_menu.run()

curses.wrapper(main)
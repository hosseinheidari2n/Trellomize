import curses
import manage
import os
import tempfile
from curses import wrapper
import re

# def add_update(self, user:manage.User):
#         # Create a temporary file and open it with the system's default editor
#         with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
#             tf.close()
#             os.system(f"{os.getenv('EDITOR', 'vim')} {tf.name}")

# def main(stdscr):
# 	stdscr.clear()
# 	stdscr.refresh()
# 	# stdscr.getch()
# 	# u1 = manage.User("bruh", 12345)
# 	# add_update(u1)
# 	with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
# 	    tf.close()
# 	    os.system(f"{os.getenv('EDITOR', 'vim')} {tf.name}")
# wrapper(main)

print(bool(re.match(f'{'hello'}', 'hello')))

def main(stdscr):
    curses.curs_set(0)
    while True:
    	print(stdscr.getch())

curses.wrapper(main)

#tab is 9 enter is 10
import curses
import os
# import manage
# import os
# import tempfile
from curses import wrapper
from curses.textpad import Textbox, rectangle
# import re
import json
import unittest

class TestDeserializing(unittest.TestCase):
    def test_comment_deserialization(self):
        pass
        





# # def add_update(self, user:manage.User):
# #         # Create a temporary file and open it with the system's default editor
# #         with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
# #             tf.close()
# #             os.system(f"{os.getenv('EDITOR', 'vim')} {tf.name}")

# # def main(stdscr):
# # 	stdscr.clear()
# # 	stdscr.refresh()
# # 	# stdscr.getch()
# # 	# u1 = manage.User("bruh", 12345)
# # 	# add_update(u1)
# # 	with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
# # 	    tf.close()
# # 	    os.system(f"{os.getenv('EDITOR', 'vim')} {tf.name}")
# # wrapper(main)

# # class bayby():
# #     def __init__(self):
# #         self.name = "navid"
# #     def toJSON(self):
# #         return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
# #     def save(self):
# #         path = 'bayby.json'
# #         with open(path, 'w') as file:
# #             json.dump(self.toJSON(), file)
# # print(bool(re.match(f'{'hello'}', 'hello')))


# class Bro:
#     def __init__(self, name):
#         self.name = name
#         self.bros = []
        
#     def addBro(self, bro):
#         self.bros.append(bro)
        
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True)
    
#     def save_project(self, path=None):
#         if path == None:
#             path = f"{self.name}.json"
#         with open(path, 'w') as file:
#             json.dump(self.toJSON(), file)

# # class things(d):
# def dict_to_object(d):    
#     return json.loads(json.dumps(d), object_hook=object)

# def main():
#     bro1 = Bro('mamad')
#     bro2 = Bro('hamed')
#     bro3 = Bro('bagher')
#     bro1.addBro(bro2)
#     bro2.addBro(bro3)
#     bro1.save_project()
#     with open('mamad.json', 'r') as file:
#         dict1 = json.load(file)
#     bro4 = dict_to_object(dict1)
#     print(json.loads(bro4))
        
    
    
    
# main()

def list_files(path):
    list1 = []
    print(str(os.walk(path)))
    for r, useless, files in os.walk(path):
        print('a')
        for file in files:
            list1.append(os.path.join(r, file).replace('\\', '/'))
    return list1

print(list_files('./testing'))
# #tab is 9 enter is 10 backspace is 8 delete is 462
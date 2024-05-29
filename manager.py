import os
import manage
import sys
import shutil
import argparse



def delete_recursive(dir_path: str): 
    try:
        shutil.rmtree(dir_path)
        print(f"successfully removed \"{dir_path}\"")
    except FileNotFoundError:
        print(f'Could not find directory: "{dir_path}"')
        return False
    except Exception as e:
        print(f'Failed to delete directory; {e}')
        
def erase_folder_content(dir_path: str):
    delete_recursive(dir_path)
    os.makedirs(dir_path)

def create_admin(username: str, password: str):
    with open('supersecret.txt', 'w') as file:
        file.write(manage.CalculateHash(username + password))

def admin_command(txt: str):
    pass
    
    
    
#~~~~~~
parser = argparse.ArgumentParser(description="Create and save system administrator.")
parser.add_argument('create-admin')
parser.add_argument('--password', required = True)
parser.add_argument('--username', required = True)

c_args = parser.parse_args()
print('create-admin' in c_args)
if 'create-admin' in c_args:
    create_admin(c_args.username, c_args.password)

if len(sys.argv) > 1 and sys.argv[1] == 'purge-data':
    # try:
        # with open('supersecret.txt', 'r') as file:
        #     if manage.CalculateHash(c_args.username + c_args.password) == file.read(0):
    erase_folder_content('users')
    erase_folder_content('logs')
    erase_folder_content('projects')
            # else:
            #     print('incorrect username or password.')
    if sys.argv[1] == 'imitate-arch':
        delete_recursive('')



    
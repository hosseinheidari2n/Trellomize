import datetime
import hashlib
import os
import uuid
import random
from enum import Enum


class User:
    def __init__(self, username, password, id = None):
        self.UserName = username
        self.Password = password
        if id == None:
            self.ID = uuid.uuid1()
        else:
            seld.ID = id
class Client:
    def __init__(self, userName, password):
        self.UserName = userName
        self.Password = password
#-----------------------------------
class Manager:
    def __init__(self, userName, password):
        self.UserName = userName
        self.Password = password
#-----------------------------------
def FirstCommandList():
    print("Hello, Welcome to our Project Management.")
    print("1. Create Manager")
    print("2. Login as Manager")
    print("3. Sign In as Client")
    print("4. Login as Client")
    print("Please enter a number between 1 to 4...")
    n = input()
    if n == "1":
        CreateManager()
    elif n == "2":
        LoginManager()
    elif n == "3":
        create_client()
    elif n == "4":
        LoginClient()
    else:
        print("Please enter a number between 1 to 4...")
        FirstCommandList()

#-------------------------------
def CreateManager():
    filePath = "manager.txt"

    if os.path.exists(filePath):
        print("Manager has been Created!")
        input("Press any key...")
        FirstCommandList()
    else:
        print("Please enter your userName...")
        userName = input()
        print("Please enter your password...")
        password1 = input()
        password = HashPassword(password1)
        manager = Manager(userName, password)

        content = f"{manager.UserName} : {manager.Password}\n"

        with open("manager.txt", "a") as file:
            file.write(content)

        print("Saved in manager.txt")
        input("Press any enter...")
        FirstCommandList()
#-------------------------------------------------------
def LoginManager():
    filePath = "manager.txt"

    if os.path.exists(filePath):
        print("Please enter your userName...")
        userName = input()
        print("Please enter your password...")
        password1 = input()
        password = CalculateHash(password1)

        with open(filePath, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    storedUsername = parts[0].strip()
                    storedPasswordHash = parts[1].strip()

                    if storedUsername == userName and storedPasswordHash == password:
                        SecondCommandList()
                        return

            print("UserName or Password is not correct")
            LoginManager()
    else:
        print("First Create Manager!")
#---------------------------------------------------------
def create_client():
    print("Please enter your userName...")
    input_username = input()
    print("Please enter your password...")
    password1 = input()
    input_password = HashPassword(password1)

    file_path = "client.txt"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

        found = False

        for line in lines:
            part = line.split(':')
            if len(part) == 2 and part[0].strip() == input_username:
                found = True
                break

        if not found:
            # Username not found, so add it
            client = Client(input_username, input_password)

            content = f"{client.UserName} : {client.Password}\n"

            with open(file_path, "a") as file:
                file.write(content)

            print("Saved in client.txt")
        else:
            # Username already exists
            print("This username exists. Please enter another username.")
            create_client() # Call the function again to get a new username

        print("Press enter to continue...")
        input()
        FirstCommandList()
    else:
        client = Client(input_username, input_password)
        content = f"{client.UserName} : {client.Password}\n"
        with open(file_path, "a") as file:
            file.write(content)
        print("Saved in client.txt")
        print("Press enter to continue...")
        input()
        FirstCommandList()

#------------------------------------------------------------

def LoginClient():
    filePath = "client.txt"

    users = {}

    try:
        with open(filePath, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    username = parts[0].strip()
                    password = parts[1].strip()
                    users[username] = password
    except Exception as e:
        print("Error: " + str(e))

    print("Please enter your userName...")
    inputUsername = input()
    print("Please enter your password...")
    inputPassword = input()

    if inputUsername in users and users[inputUsername] == CalculateHash(inputPassword):
        SecondCommandList()
    else:
        print("UserName or Password is not correct")
        LoginClient()
#--------------------------------------------------------------
def HashPassword(password):
    passwordBytes = password.encode('utf-8')
    hashBytes = hashlib.sha256(passwordBytes).digest()
    return hashBytes.hex()
#----------------------------------------------------------------
def CalculateHash(input):
    hashBytes = hashlib.sha256(input.encode('utf-8')).digest()
    return hashBytes.hex()
#----------------------------------------------------------------
def SecondCommandList():
    print("1. Create Project")
    print("2. Show Projects")

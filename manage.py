import hashlib
import os


class Client:
    def __init__(self, userName, password):
        self.UserName = userName
        self.Password = password

class Manager:
    def __init__(self, userName, password):
        self.UserName = userName
        self.Password = password

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
        CreateClient()
    elif n == "4":
        LoginClient()
    else:
        print("Please enter a number between 1 to 4...")
        FirstCommandList()

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

def CreateClient():
    print("Please enter your userName...")
    userName = input()
    print("Please enter your password...")
    password1 = input()
    password = HashPassword(password1)

    client = Client(userName, password)

    content = f"{client.UserName} : {client.Password}\n"

    with open("client.txt", "a") as file:
        file.write(content)

    print("Saved in client.txt")
    input("Press any enter...")
    FirstCommandList()

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

def HashPassword(password):
    passwordBytes = password.encode('utf-8')
    hashBytes = hashlib.sha256(passwordBytes).digest()
    return hashBytes.hex()

def CalculateHash(input):
    hashBytes = hashlib.sha256(input.encode('utf-8')).digest()
    return hashBytes.hex()

def SecondCommandList():
    print("1. Create Project")
    print("2. Show Projects")

if __name__ == "__main__":
    FirstCommandList()

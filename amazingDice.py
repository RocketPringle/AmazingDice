# ------ MODULES ------ #

width = 9

import random  # imports random module for dice rolls
import time  # imports time module for delays and animations
import json  # imports json module for user data storage
import os  # imports os module for file operations
import hashlib  # imports hashlib module for password hashing
import amazingDiceGUI as adGUI  # imports GUI module

# ------ FILE STUFF ------ #

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # changes to scripts directory for file operations

# ------ USER DATA FUNCTIONS ------ #

def hashPassword(password):  # defines function to hash passwords using SHA256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()  # returns password as hashed version ig idk

def loadUsers():  # defines function to load user data from JSON file
    try:
        with open('userLoginInfo.json', 'r') as file:  # attempts to open user data file
            return json.load(file)  # returns user data as dictionary
    except FileNotFoundError:  # handles case where file doesnt exist
        print("Warning User data file not found Creating temporary user structure")  # prints warning message
        return {"users": {}}  # returns empty user structure
    except PermissionError:  # handles case where file cant be accessed
        print("Error Cannot access user data file Creating temporary user structure")  # prints error message
        return {"users": {}}  # returns empty user structure
    except json.JSONDecodeError:  # handles case where file is corrupted
        print("Error User data file is corrupted Creating temporary user structure")  # prints error message
        return {"users": {}}  # returns empty user structure

def saveUsers(data):  # defines function to save user data to JSON file
    try:
        with open('userLoginInfo.json', 'w') as file:  # opens file in write mode
            json.dump(data, file, indent=4)  # writes data to file with formatting
    except PermissionError:  # handles case where file cant be written
        print("Error Cannot save user data Check file permissions")  # prints error message

def addNewUser(username, password):  # defines function to add new user to system
    data = loadUsers()  # loads current user data
    
    if username in data['users']:  # checks if username already exists
        print("Username already exists")  # prints error message
        return False  # returns False if username exists
    
    data['users'][username] = {  # creates new user entry
        "hashedPassword": hashPassword(password),  # stores hashed password
        "joinDate": time.strftime("%d/%m/%Y"),  # stores join date in UK format
        "stats": {  # initializes user statistics
            "totalGames": 0,  # total games played
            "wins": 0,  # total wins
            "losses": 0,  # total losses
            "draws": 0,  # total draws
            "vsBot": {  # stats for bot matches
                "easy": {  # easy difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "medium": {  # medium difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "hard": {  # hard difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "expert": {  # expert difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                }
            },
            "vsPlayer": {  # stats for player vs player matches
                "wins": 0,
                "losses": 0,
                "draws": 0
            }
        }
    }
    
    saveUsers(data)  # saves updated user data
    print(f"\nUser {username} created successfully\n")  # prints success message
    return True  # returns True if user created successfully

def getStats(username):  # defines function to get user statistics
    data = loadUsers()  # loads user data
    stats = data['users'][username]['stats']  # gets users stats
    return stats  # returns stats dictionary

def login(username, password):  # defines function to handle user login
    userData = loadUsers()  # loads user data
    print('loaded user data')  # prints debug message
    
    if username in userData['users']:  # checks if username exists
        if userData['users'][username]['hashedPassword'] == hashPassword(password):  # checks if password is correct
            return username  # returns username if login successful
        else:
            print("Incorrect password")  # prints error for wrong password
            return False  # returns False for failed login
    else:
        print("Username not found")  # prints error for missing username
        return False  # returns False for failed login

def createAccount(username, password):  # defines function to create new account
    userData = loadUsers()  # loads user data
    if username in userData['users']:  # checks if username exists
        print('Username already exists\nTry a different username')  # prints error message
        createAccount(username, password)  # recursively tries again
    while not (len(password) >= 12 and  # checks password requirements
              any(c.isdigit() for c in password) and  # must have number
              any(c.isupper() for c in password) and  # must have uppercase
              any(c.islower() for c in password) and  # must have lowercase
              any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)):  # must have special character
        print("Password must be at least 12 characters and contain uppercase lowercase numbers and special characters")  # prints requirements
    if addNewUser(username, password):  # attempts to add new user
        print(f"Account created successfully Welcome {username}")  # prints success message
        return username  # returns username if successful

# ------ GAME FUNCTIONS ------ #

def diceRoll(size, difficulty):
    roll = random.randint(1,size) + difficulty
    if roll < 0:
        return 0
    else:
        return roll
    
    

def playRound(size, difficulty):
    startRoll1, startRoll2 = diceRoll(size, 0), diceRoll(size, difficulty)
    rolls1, rolls2 = [], []
    for i in range(0, 3): # 3 rolls each
        rolls1.append(diceRoll(size, 0)) # roll for player 1
        rolls2.append(diceRoll(size, difficulty)) # roll for player 2
        #rollTotal1, rollTotal2 += rolls1[i+1], rolls2[i+1] # add the roll to the total
    return rolls1, rolls2, sum(rolls1), sum(rolls2), startRoll1 > startRoll2
        

        
        



def getDifficultyInt(difficulty):  # defines function to convert difficulty number to string
    if difficulty == 'easy':
        return -2
    elif difficulty == 'medium':
        return -1
    elif difficulty == 'hard':
        return 0
    else:
        return 1  
    


# ------ MAIN ------ #

if __name__ == "__main__":  # checks if file is being run directly
    adGUI.home()  # starts GUI application

# ONLINE:??????????????

# sign up:
    # make user + pass (pass can be random and has to be 12 chars, capital and lowercase, special char)
# log in:
    # get username + pass 
# guest
    # no acc

# show menu:
    # stats choice ✔
    # match with other (who signs in) or bot (difficulties make bot roll more times? or have buffed odds ig idk this ist skil based bro) ✔
    # logout ✔

# stats choice:
    # use file management to show stats

# match choice:
    # person:
        # other player sign in or guest (no acc)
        # do first roll to determine first ppl draws etc
        # roll 3 times and total for each person
        # if draw, roll again
        # whoever largest gets point stored in dict
        # find largest points
        # print ascii art trophy with score under
    # bot:
        # difficulties:
            # easy does score but -2 ✔
            # med does score but -1 ✔  
            # hard does score but -0 ✔
            # expert does score but +1 ✔
        # both roll 3 times and total for each person but bot -x based on difficulty
        # if draw, roll again
        # whoever largest gets point stored in dict
        # find largest points
        # print ascii art trophy with score under
        